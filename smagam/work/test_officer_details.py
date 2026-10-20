from pathlib import Path
s=Path('work/viewer-pdf.html').read_text(encoding='utf-8')
def fn(name):
 start=s.index('function '+name+'(');end=s.index('\nfunction ',start+10);return s[start:end]
code="""const assert=require('node:assert/strict');const DEP_TYPES={officer:'Police officer',gate:'Gate duty'};const depEsc=v=>String(v).replaceAll('&','&amp;').replaceAll('<','&lt;').replaceAll('>','&gt;').replaceAll('"','&quot;');let depUnits=[],conceptItems=[],simulationOn=false,depDrawnOfficers=[];const worldFacilities=new Map();
"""+'\n'.join(fn(n) for n in ['depDutyLocation','depOfficerRows','depCollectExistingOfficers'])+"""
const u={title:'Gate 2',type:'officer',ground:'B',position:[1,0,2],personnel:[{name:'Test <name>',rank:'SI',contact:'0000000000',role:'Access checking'}]};assert.match(depOfficerRows(u),/Mobile: 0000000000/);assert.match(depOfficerRows(u),/Test &lt;name&gt;/);assert.match(depDutyLocation(u),/Ground B/);u.location='Gate 2 entry';assert.equal(depDutyLocation(u),'Gate 2 entry');assert.match(depOfficerRows({...u,personnel:[]}),/Mobile: Not assigned/);
conceptItems=[{id:'G01',category:'gate',world:[10,0,20],name:'Gate 1'},{id:'S04',category:'traffic',world:[50,0,20],name:'Footbridge'}];worldFacilities.set('B17',{point:p=>p,item:{layer:'services'}});simulationOn=true;depDrawnOfficers=[{key:'deployed1',p:[1,0,1]}];const rows=depCollectExistingOfficers();assert.equal(rows.size,13);assert.equal(rows.get('CHOWKI-0').location,'Police chowki');assert.equal(rows.get('GATE-G01--1').duty,'Gate security / access checking');assert.equal(depUnits.length,0);console.log('PASS: duty location, mobile, escaping, unassigned fields and 13 existing/deployed officer icon anchors; no force records added');
"""
Path('work/test-officer-details.cjs').write_text(code,encoding='utf-8')
