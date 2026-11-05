'use strict';
const CFG={N:22,HALF:11,TICKS:1100,TAU_MUD:.38,VOTE_NEED:2,B_MAX:4,C_MAX:8,LAMBDA_V:1.0,LAMBDA_M:.15};
const PARTS=[{k:'all',n:'全景'},{k:'C',n:'小龙虾·嬉'},{k:'B',n:'波龙·惕'},{k:'S',n:'调度器'},{k:'M',n:'记忆池'},{k:'T',n:'地形'}];
const VIEWS=[{k:'hero',n:'主视角'},{k:'top',n:'俯视'},{k:'side',n:'侧视'},{k:'inside',n:'岩隙内'}];
function mulberry32(a){return function(){a|=0;a=a+0x6D2B79F5|0;let t=Math.imul(a^a>>>15,1|a);t=t+Math.imul(t^t>>>7,61|t)^t;return((t^t>>>14)>>>0)/4294967296}}
const clamp=(v,a,b)=>v<a?a:v>b?b:v;
function makeField(p){
  const peaks=[
    {x:6.2,z:-5.8,a:1.00,s:2.30,label:'岩礁之隙 · 全局最优'},
    {x:-7.2,z:5.4,a:.74,s:2.70,label:'次优峰'},
    {x:1.8,z:7.2,a:.58,s:1.70,label:'局部陷阱'}];
  if(p.complexity>.35)peaks.push({x:-7.8,z:-6.6,a:.46,s:1.50,label:'诱饵 D'});
  if(p.complexity>.70)peaks.push({x:8.2,z:6.8,a:.40,s:1.40,label:'诱饵 E'});
  const hazards=[{x:-2.6,z:-2.2,r:2.5},{x:4.2,z:3.4,r:1.9},{x:-8.4,z:-7.2,r:1.7}];
  if(p.complexity>.55)hazards.push({x:1.0,z:-8.5,r:1.6});
  const grow=1+p.stress*.95;
  hazards.forEach(h=>h.r*=grow);
  return{peaks,hazards,riskScale:.55+p.risk*1.05,gmax:0};
}
function fval(F,x,z){
  let v=0;
  for(const p of F.peaks){const d2=(x-p.x)**2+(z-p.z)**2;v+=p.a*Math.exp(-d2/(2*p.s*p.s));}
  v+=.045*Math.sin(.85*x)*Math.cos(.72*z);
  return clamp(v,0,1);
}
function risk(F,x,z){
  let r=0;
  for(const h of F.hazards)r=Math.max(r,Math.max(0,1-Math.hypot(x-h.x,z-h.z)/h.r));
  const edge=Math.max(Math.abs(x),Math.abs(z))/CFG.HALF;
  r=Math.max(r,Math.max(0,(edge-.86)/.14)*.55);
  return clamp(r*F.riskScale,0,1);
}
const height=(F,x,z)=>fval(F,x,z)*2.35;
function globalMax(F){
  let g=0;
  for(let i=0;i<=CFG.N;i++)for(let j=0;j<=CFG.N;j++){
    const x=-CFG.HALF+i*2*CFG.HALF/CFG.N,z=-CFG.HALF+j*2*CFG.HALF/CFG.N;
    if(risk(F,x,z)<.35)g=Math.max(g,fval(F,x,z));
  }
  return g;
}
function simulate(p){
  const F=makeField(p);F.gmax=globalMax(F);
  const rnd=mulberry32(20261105);
  const ex=new Uint8Array(CFG.N*CFG.N);
  const gi=(x,z)=>{const i=Math.floor((x+CFG.HALF)/(2*CFG.HALF)*CFG.N),j=Math.floor((z+CFG.HALF)/(2*CFG.HALF)*CFG.N);return i>=0&&i<CFG.N&&j>=0&&j<CFG.N?i*CFG.N+j:-1};
  const isEx=(x,z)=>{const k=gi(x,z);return k>=0&&ex[k]===1};
  const mark=(x,z,r)=>{for(let dx=-r;dx<=r;dx+=.85)for(let dz=-r;dz<=r;dz+=.85){if(dx*dx+dz*dz>r*r)continue;const k=gi(x+dx,z+dz);if(k>=0)ex[k]=1;}};
  const agents=[];
  for(let i=0;i<CFG.C_MAX;i++)agents.push({id:'C'+i,kind:'C',x:-8.6+rnd()*2.2,z:8.4-rnd()*2.2,state:'Wander',active:i<6,task:null,dwell:0,votes:0});
  for(let i=0;i<CFG.B_MAX;i++)agents.push({id:'B'+i,kind:'B',x:-1+rnd()*2,z:-1+rnd()*2,state:'Idle',active:i<1,task:null,dwell:0,votes:0});
  const w={t:0,agents,caves:[],reefs:[],tasks:[],events:[],trails:[],timeline:[],
    best:0,prevBest:0,lastImprove:0,violations:0,abandoned:0,migration:0,vioT:0,migT:0,caveSeq:0,peak:F.peaks[0]};
  const log=(kind,text)=>{w.events.push({t:w.t,kind,text});if(w.events.length>90)w.events.shift();};
  const task=(type,label,assignee,dep)=>{const o={id:'T'+(w.tasks.length+1),type,label,assignee,dep,status:'pending'};w.tasks.push(o);return o};
  task('MAP','空间探索 · 全域覆盖','C-pool','—').status='active';
  task('DISCOVER','候选发现 · 淤泥窟标记','C-pool','T1').status='active';
  task('REPORT','结果汇总 · 输出可行解','A_S','T2');
  mark(-8.6,8.4,2.2);
  log('s','A_S 初始化：6 探索机 + 1 求精机，任务 MAP / DISCOVER 已激活');
  const setCounts=(wc,wb)=>{
    let c=0,b=0;
    for(const a of w.agents){if(a.kind==='C'){a.active=c<wc;c++;}else{a.active=b<wb;b++;}}
    for(const a of w.agents){if(!a.active&&a.task){const cc=w.caves.find(q=>q.id===a.task);if(cc)cc.assigned=null;a.task=null;a.state='Idle';}}
  };
  function scheduler(){
    const cov=w.m.coverage;
    const pending=w.caves.filter(c=>c.state==='mud'&&!c.assigned&&c.votes<CFG.VOTE_NEED);
    let wc,wb,why;
    if(cov<.26){wc=Math.min(CFG.C_MAX,6+Math.round(p.lambdaE*2));wb=1;why='低覆盖 → 扩容探索池';}
    else if(pending.length>0){wb=Math.min(CFG.B_MAX,Math.max(2,pending.length));wc=Math.max(3,7-Math.floor(wb/2));why='候选积压 → 增派求精机并做多机共识';}
    else{wc=Math.max(3,Math.round(7-cov*3));wb=1;why='稳态 → 收缩探索、维持警戒';}
    if(p.stress>.55)wb=Math.max(1,wb-1);
    if(p.stress>.85){wb=1;why='高压 → 求精池收缩，共识放缓';}
    setCounts(wc,wb);
    const idle=w.agents.filter(a=>a.kind==='B'&&a.active&&!a.task);
    for(const b of idle){
      const c=pending.shift();if(!c)break;
      c.assigned=b.id;b.task=c.id;b.target={x:c.x,z:c.z};b.state='Migrate';b.dwell=0;
      const t=w.tasks.find(q=>q.type==='VERIFY'&&q.cid===c.id);if(t){t.status='active';t.assignee=b.id;}
      log('s','派发 '+c.id+' → '+b.id+'（VERIFY · 约束核验与局部求精）');
      w.migT++;
    }
    if(w.t-w.lastImprove>105&&w.t>60){
      let bi=0,best=-1;
      for(let q=0;q<4;q++){const cx=(q%2?1:-1)*6,cz=(q<2?1:-1)*6;let u=0;for(let d=-2;d<=2;d++)if(!isEx(cx+d,cz))u++;if(u>best){best=u;bi=q;}}
      const cs=w.agents.filter(a=>a.kind==='C'&&a.active);
      if(cs.length){const a=cs[Math.floor(rnd()*cs.length)];a.x=(bi%2?1:-1)*6;a.z=(bi<2?1:-1)*6;w.lastImprove=w.t;log('s','收益停滞 → 触发全域重采样，'+a.id+' 迁移至低覆盖象限');w.migT+=2;}
    }
    w.m.decision=why;
  }
  function stepC(a){
    let bt=0,bs=-1e9,bu=0;
    for(let k=0;k<8;k++){
      const th=k*Math.PI/4+rnd()*.45;
      const nx=a.x+Math.cos(th)*2.3,nz=a.z+Math.sin(th)*2.3;
      if(Math.abs(nx)>CFG.HALF-.5||Math.abs(nz)>CFG.HALF-.5)continue;
      let un=0;
      for(let s=-1;s<=1;s++)for(let t=-1;t<=1;t++)if(!isEx(nx+s,nz+t))un++;
      const sc=un+fval(F,nx,nz)*1.5-risk(F,nx,nz)*2.4+rnd()*p.lambdaE*8;
      if(sc>bs){bs=sc;bt=th;bu=un;}
    }
    const st=.40+.24*rnd()*(.6+p.lambdaE);
    let nx=clamp(a.x+Math.cos(bt)*st,-CFG.HALF+.4,CFG.HALF-.4),nz=clamp(a.z+Math.sin(bt)*st,-CFG.HALF+.4,CFG.HALF-.4);
    if(risk(F,nx,nz)>.78){nx=a.x-Math.cos(bt)*st*.6;nz=a.z-Math.sin(bt)*st*.6;w.violations++;w.vioT++;a.state='Evade';}
    else a.state=bu>3?'Wander':'MarkCave';
    a.x=nx;a.z=nz;
    mark(nx,nz,1.75);
    const val=fval(F,nx,nz);
    if(val>CFG.TAU_MUD){
      const near=w.caves.some(c=>Math.hypot(c.x-nx,c.z-nz)<2.3)||w.reefs.some(c=>Math.hypot(c.x-nx,c.z-nz)<2.3);
      if(!near){
        const c={id:'H'+(++w.caveSeq),x:nx,z:nz,score:val,state:'mud',votes:0,voters:{},assigned:null,at:w.t};
        w.caves.push(c);
        const t=task('VERIFY','可行性核验 · '+c.id,'pending','T2');t.cid=c.id;t.status='pending';
        log('c',a.id+' 发现 '+c.id+'  f='+val.toFixed(3)+' → 写入淤泥窟，生成 VERIFY 任务');
      }
    }
    if(w.t%3===0)w.trails.push({t:w.t,id:a.id,kind:'C',x:nx,z:nz});
  }
  function stepB(a){
    const c=w.caves.find(q=>q.id===a.task);
    if(!c){a.state='Idle';return;}
    if(a.state==='Migrate'){
      const dx=c.x-a.x,dz=c.z-a.z,d=Math.hypot(dx,dz);
      if(d>.55){a.x+=dx/d*.62;a.z+=dz/d*.62;w.migT++;}
      else{a.state='DigLocal';a.dwell=0;log('b',a.id+' 抵达 '+c.id+' → DigLocal 局部梯度上升');}
    }else if(a.state==='DigLocal'){
      const e=.28;
      const gx=(fval(F,a.x+e,a.z)-fval(F,a.x-e,a.z))/(2*e);
      const gz=(fval(F,a.x,a.z+e)-fval(F,a.x,a.z-e))/(2*e);
      const rx=(risk(F,a.x+e,a.z)-risk(F,a.x-e,a.z))/(2*e);
      const rz=(risk(F,a.x,a.z+e)-risk(F,a.x,a.z-e))/(2*e);
      let nx=a.x+.22*gx-.45*rx,nz=a.z+.22*gz-.45*rz;
      if(risk(F,nx,nz)>.46){
        nx=a.x-.14*gx-.30*rx;nz=a.z-.14*gz-.30*rz;
        w.violations++;w.vioT++;a.state='VigilScan';
      }
      a.x=clamp(nx,-CFG.HALF+.4,CFG.HALF-.4);a.z=clamp(nz,-CFG.HALF+.4,CFG.HALF-.4);
      c.x=a.x;c.z=a.z;
      const v=fval(F,a.x,a.z);
      if(v>c.score+.002){c.score=v;w.lastImprove=w.t;}
      if(++a.dwell>13)a.state='VigilScan';
    }else if(a.state==='VigilScan'||a.state==='Evade'){
      let projSteps=0;
      while(risk(F,a.x,a.z)>=.28&&projSteps<3){
        const e=.30;
        const rx=(risk(F,a.x+e,a.z)-risk(F,a.x-e,a.z))/(2*e);
        const rz=(risk(F,a.x,a.z+e)-risk(F,a.x,a.z-e))/(2*e);
        const n=Math.hypot(rx,rz)||1;
        a.x=clamp(a.x-rx/n*.26,-CFG.HALF+.4,CFG.HALF-.4);
        a.z=clamp(a.z-rz/n*.26,-CFG.HALF+.4,CFG.HALF-.4);
        projSteps++;
      }
      w.vioT+=projSteps;
      c.x=a.x;c.z=a.z;
      const v=fval(F,a.x,a.z);
      if(v>c.score+.002){c.score=v;w.lastImprove=w.t;}
      const feas=risk(F,a.x,a.z)<.34&&projSteps<3;
      const seen=c.voters[a.id]||0;
      if(seen<2){c.voters[a.id]=seen+1;if(feas)c.votes++;}
      c.tries=(c.tries||0)+1;
      log('b',a.id+' 警戒扫描 '+c.id+'：'+(feas?'可行 +1 票':'约束投影 '+projSteps+' 步')+'（'+c.votes+'/'+CFG.VOTE_NEED+'）');
      const vt=w.tasks.find(q=>q.type==='VERIFY'&&q.cid===c.id);
      if(c.votes>=CFG.VOTE_NEED&&feas&&c.state==='mud'){
        c.state='reef';w.reefs.push({x:c.x,z:c.z,score:c.score,t:w.t,id:c.id});
        w.best=Math.max(w.best,c.score);w.lastImprove=w.t;
        if(vt)vt.status='done';
        const rt=task('REFINE','局部求精 · '+c.id,a.id,'T2');rt.status='done';
        const tt=w.tasks.find(q=>q.type==='REPORT');
        if(tt&&w.best>=F.gmax*.94&&tt.status!=='done'){
          tt.status='done';
          log('s','任务闭环：REPORT 完成，已求得全局可行解 f='+w.best.toFixed(3));
        }
        log('s','多机共识达成 → '+c.id+' 升级为岩礁隙，可行解 '+c.score.toFixed(3));
        c.assigned=null;a.task=null;a.state='Idle';
      }else if(projSteps>=3||(c.votes===0&&c.tries>=3)){
        c.state='abandoned';w.abandoned++;
        if(vt)vt.status='done';
        log('b','高冲突区域 → Abandon，'+c.id+' 降权，交还探索池');
        c.assigned=null;a.task=null;a.state='Idle';
      }else{
        c.assigned=null;a.task=null;a.state='Idle';
      }
    }
    if(w.t%3===0)w.trails.push({t:w.t,id:a.id,kind:'B',x:a.x,z:a.z});
  }
  for(let tick=0;tick<CFG.TICKS;tick++){
    w.t=tick;w.vioT=0;w.migT=0;
    let nEx=0;for(let i=0;i<ex.length;i++)nEx+=ex[i];
    w.m={coverage:nEx/ex.length,NC:0,NB:0,best:w.best,decision:'',t:tick};
    for(const a of w.agents)if(a.active)w.m[a.kind==='C'?'NC':'NB']++;
    if(tick%16===0)scheduler();
    for(const a of w.agents)if(a.active){if(a.kind==='C')stepC(a);else stepB(a);}
    const Cs=w.agents.filter(a=>a.kind==='C'&&a.active);
    const spread=Cs.reduce((s,a)=>s+Math.hypot(a.x+7.5,a.z-7.5),0)/Math.max(1,Cs.length);
    const ent=clamp(spread/16,0,1);
    const rObj=(w.best-w.prevBest)*100;
    const Cv=w.vioT*.30,Cm=w.migT*.35;
    const reward=rObj-CFG.LAMBDA_V*Cv+p.lambdaE*ent-CFG.LAMBDA_M*Cm;
    w.prevBest=w.best;
    const taskDone={},taskActive={};
    for(const tk of w.tasks){
      if(tk.status==='done')taskDone[tk.type]=(taskDone[tk.type]||0)+1;
      else if(tk.status==='active')taskActive[tk.type]=(taskActive[tk.type]||0)+1;
    }
    Object.assign(w.m,{
      entropy:ent,reward,violations:w.violations,migration:w.migration+w.migT*.02,
      discovered:w.caves.length,reefs:w.reefs.length,abandoned:w.abandoned,
      feasibleRatio:w.reefs.length/Math.max(1,w.reefs.length+w.abandoned),
      solved:w.best>=F.gmax*.94,
      bestScore:w.best,gmax:F.gmax,
      taskDone,taskActive,frontier:0
    });
    w.migration+=w.migT*.02;
    w.timeline.push({
      t:tick,ex:ex.slice(),
      agents:w.agents.map(a=>({id:a.id,kind:a.kind,x:a.x,z:a.z,state:a.state,active:a.active,task:a.task})),
      caves:w.caves.map(c=>({id:c.id,x:c.x,z:c.z,score:c.score,state:c.state,votes:c.votes,at:c.at})),
      reefs:w.reefs.map(r=>({...r})),
      tasks:w.tasks.slice(-10).map(t=>({...t})),
      events:w.events.slice(-34).map(e=>({...e})),
      m:{...w.m}
    });
  }
  return{F,timeline:w.timeline,trails:w.trails,gmax:F.gmax,peak:F.peaks[0]};
}
