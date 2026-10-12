import { readFileSync } from 'node:fs';
const S = JSON.parse(readFileSync(process.argv[2], 'utf8')).species;
const RW = { common: 55, uncommon: 30, rare: 12, very_rare: 3 };
const t = [];
for (const s of S) for (const e of s.encounters ?? []) t.push([(e.min + e.max) / 2, s.bst, RW[e.rarity] ?? 10, e.area]);
function fit(rows){let sw=0,sx=0,sy=0,sxx=0,sxy=0;for(const [x,y,w] of rows){sw+=w;sx+=w*x;sy+=w*y;sxx+=w*x*x;sxy+=w*x*y;}const b=(sw*sxy-sx*sy)/(sw*sxx-sx*sx);const a=(sy-b*sx)/sw;return [a,b];}
const [a,b]=fit(t); console.log('a',a.toFixed(1),'b',b.toFixed(2),'L30',(a+b*30).toFixed(1),'L47',(a+b*47).toFixed(1),'L60',(a+b*60).toFixed(1));
const mine=t.filter(r=>r[3]?.startsWith('wickrun')); const avg=(f)=>{let s=0,w=0;for(const r of mine.filter(f)){s+=r[1]*r[2];w+=r[2]}return (s/w).toFixed(0)}; console.log('mine night', avg(r=>r[0]<55), 'day', avg(r=>r[0]>=55));
