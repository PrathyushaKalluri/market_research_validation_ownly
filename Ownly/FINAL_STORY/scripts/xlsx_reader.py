import zipfile,re,sys,xml.etree.ElementTree as ET
ns={'m':'http://schemas.openxmlformats.org/spreadsheetml/2006/main'}
def read(f):
    z=zipfile.ZipFile(f); ss=[]
    if 'xl/sharedStrings.xml' in z.namelist():
        for si in ET.fromstring(z.read('xl/sharedStrings.xml')).findall('m:si',ns):
            ss.append(''.join(t.text or '' for t in si.iter('{%s}t'%ns['m'])))
    wb=ET.fromstring(z.read('xl/workbook.xml'))
    names=[s.get('name') for s in wb.find('m:sheets',ns)]
    out={}
    for i,n in enumerate(names,1):
        p=f'xl/worksheets/sheet{i}.xml'
        if p not in z.namelist(): continue
        rows=[]
        for r in ET.fromstring(z.read(p)).iter('{%s}row'%ns['m']):
            row={}
            for c in r.findall('m:c',ns):
                col=re.match(r'[A-Z]+',c.get('r')).group(); v=c.find('m:v',ns); t=c.get('t')
                if t=='s' and v is not None: val=ss[int(v.text)]
                elif t=='inlineStr': val=''.join(x.text or '' for x in c.iter('{%s}t'%ns['m']))
                else: val=v.text if v is not None else ''
                row[col]=val
            rows.append(row)
        out[n]=rows
    return out
if __name__=='__main__':
    for f in sys.argv[1:]:
        for n,rows in read(f).items():
            print('==',f,n,len(rows))
            for r in rows[:int(sys.argv[0:1] and 400)]: print(r)
