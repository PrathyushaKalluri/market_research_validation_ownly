#!/usr/bin/env python3
"""
Tableau workbook generator.

Emits a .twb (XML) and packages it with ./Data into a .twbx.
Worksheets are declared with a compact spec; the XML boilerplate is generated.

This is the part Tableau is fussiest about, so the generator keeps the XML
canonical and minimal rather than clever.
"""

import csv, os, zipfile, html

HERE = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(HERE, "Data")

# ── datatype inference for the CSV column declarations ──────────────
def sniff(path):
    with open(path, encoding="utf-8") as f:
        rd = csv.reader(f)
        hdr = next(rd)
        rows = [r for _, r in zip(range(400), rd)]
    types = []
    for i, name in enumerate(hdr):
        vals = [r[i].strip() for r in rows if i < len(r) and r[i].strip() != ""]
        if not vals:
            types.append("string"); continue
        allint = allnum = True
        for v in vals:
            try:
                fv = float(v)
                if fv != int(fv): allint = False
            except ValueError:
                allint = allnum = False; break
        types.append("integer" if allnum and allint else ("real" if allnum else "string"))
    return hdr, types

def esc(s): return html.escape(str(s), quote=True)

def _uuid(seed):
    """Deterministic UUID so rebuilds are stable and diffable."""
    import hashlib
    h = hashlib.md5(seed.encode("utf-8")).hexdigest().upper()
    return "%s-%s-%s-%s-%s" % (h[0:8], h[8:12], h[12:16], h[16:20], h[20:32])

# ── datasource XML ──────────────────────────────────────────────────
def datasource(ds_name, filename, caption):
    tok = ds_name.split('.', 1)[1] if '.' in ds_name else ds_name
    path = os.path.join(DATA, filename)
    hdr, types = sniff(path)
    base = filename[:-4]
    cols = "\n".join(
        "            <column datatype='%s' name='%s' ordinal='%d' />" % (t, esc(h), i)
        for i, (h, t) in enumerate(zip(hdr, types)))
    meta = "\n".join(
        "    <column datatype='%s' name='[%s]' role='%s' type='%s' />"
        % (t, esc(h), "measure" if t in ("integer", "real") else "dimension",
           "quantitative" if t in ("integer", "real") else "nominal")
        for h, t in zip(hdr, types))

    # ── metadata-records ──────────────────────────────────────────
    # Tableau's "lazy connections" datasource parser reads these to learn the
    # table's shape without opening the file. Omit them and it asserts
    # !m_activeSheet.empty() in DsParserHelper.cpp and raises 501CF476.
    REMOTE = {"string": 129, "integer": 20, "real": 5, "date": 133, "boolean": 11}
    AGG = {"string": "Count", "integer": "Sum", "real": "Sum", "date": "Year", "boolean": "Count"}
    oid = "[%s.csv_%s]" % (base, _uuid(base).replace("-", ""))
    cap_rec = (
        "        <metadata-record class='capability'>\n"
        "          <remote-name />\n"
        "          <remote-type>0</remote-type>\n"
        "          <parent-name>[%s.csv]</parent-name>\n"
        "          <remote-alias />\n"
        "          <aggregation>Count</aggregation>\n"
        "          <contains-null>true</contains-null>\n"
        "          <attributes>\n"
        "            <attribute datatype='string' name='character-set'>&quot;UTF-8&quot;</attribute>\n"
        "            <attribute datatype='string' name='collation'>&quot;en_GB&quot;</attribute>\n"
        "            <attribute datatype='string' name='field-delimiter'>&quot;,&quot;</attribute>\n"
        "            <attribute datatype='string' name='header-row'>&quot;true&quot;</attribute>\n"
        "            <attribute datatype='string' name='locale'>&quot;en_IN&quot;</attribute>\n"
        "            <attribute datatype='string' name='single-char'>&quot;&quot;</attribute>\n"
        "          </attributes>\n"
        "        </metadata-record>" % esc(base))
    col_recs = []
    for i, (h, t) in enumerate(zip(hdr, types)):
        col_recs.append(
            "        <metadata-record class='column'>\n"
            "          <remote-name>%s</remote-name>\n"
            "          <remote-type>%d</remote-type>\n"
            "          <local-name>[%s]</local-name>\n"
            "          <parent-name>[%s.csv]</parent-name>\n"
            "          <remote-alias>%s</remote-alias>\n"
            "          <ordinal>%d</ordinal>\n"
            "          <local-type>%s</local-type>\n"
            "          <aggregation>%s</aggregation>\n"
            "          <contains-null>true</contains-null>\n"
            "          <object-id>%s</object-id>\n"
            "        </metadata-record>"
            % (esc(h), REMOTE.get(t, 129), esc(h), esc(base), esc(h), i, t,
               AGG.get(t, "Count"), esc(oid)))
    metarecs = ("      <metadata-records>\n" + cap_rec + "\n"
                + "\n".join(col_recs) + "\n      </metadata-records>\n")

    return hdr, types, """  <datasource caption='%s' inline='true' name='%s' version='18.1'>
    <connection class='federated'>
      <named-connections>
        <named-connection caption='%s' name='textscan.%s'>
          <connection class='textscan' directory='Data' filename='%s' password='' server='' />
        </named-connection>
      </named-connections>
      <relation connection='textscan.%s' name='%s' table='[%s#csv]' type='table'>
        <columns character-set='UTF-8' header='yes' locale='en_IN' separator=','>
%s
        </columns>
      </relation>
%s    </connection>
%s
  </datasource>""" % (esc(caption), ds_name, esc(base), tok, esc(filename),
                      tok, esc(filename), esc(base), cols, metarecs, meta)

# ── worksheet XML ───────────────────────────────────────────────────
def inst(field, tp, agg=None):
    """Tableau column-instance naming: [none:Field:nk] / [sum:Field:qk]."""
    if tp in ("integer", "real"):
        return "[%s:%s:qk]" % (agg or "sum", field)
    return "[none:%s:nk]" % field

def worksheet(name, ds, hdr, types, rows_f, cols_f, mark="Bar",
              color=None, label=None, size=None, filters=None, sort=None, title=None):
    T = dict(zip(hdr, types))
    rows_list = rows_f if isinstance(rows_f, (list, tuple)) else ([rows_f] if rows_f else [])
    cols_list = cols_f if isinstance(cols_f, (list, tuple)) else ([cols_f] if cols_f else [])
    used = list(rows_list) + list(cols_list) + [f for f in [color, label, size] if f]
    if filters:
        used += [f[0] for f in filters]
    if sort: used.append(sort)
    seen, deps = set(), []
    for f in used:
        if f in seen or f not in T: continue
        seen.add(f)
        t = T[f]
        role = "measure" if t in ("integer", "real") else "dimension"
        typ = "quantitative" if t in ("integer", "real") else "nominal"
        deps.append("        <column datatype='%s' name='[%s]' role='%s' type='%s' />" % (t, esc(f), role, typ))
        if t in ("integer", "real"):
            deps.append("        <column-instance column='[%s]' derivation='Sum' name='%s' pivot='key' type='quantitative' />" % (esc(f), esc(inst(f, t))))
        else:
            deps.append("        <column-instance column='[%s]' derivation='None' name='%s' pivot='key' type='nominal' />" % (esc(f), esc(inst(f, t))))

    fx = ""
    if filters:
        for fld, vals in filters:
            members = "".join("<groupfilter function='member' level='[%s]' member='&quot;%s&quot;' />" % (esc(fld), esc(v)) for v in vals)
            fx += """      <filter class='categorical' column='[%s].[%s]'>
        <groupfilter function='union' user:ui-domain='relevant' user:ui-enumeration='inclusive' user:ui-marker='enumerate'>%s</groupfilter>
      </filter>\n""" % (ds, esc(fld), members)

    # Encoding children are named by encoding type — <color/>, <text/>, <size/> —
    # NOT <encoding attr='color'/>. Tableau's schema rejects the latter outright.
    enc = ""
    if color: enc += "            <color column='[%s].%s' />\n" % (ds, esc(inst(color, T.get(color, "string"))))
    if label: enc += "            <text column='[%s].%s' />\n" % (ds, esc(inst(label, T.get(label, "real"))))
    if size:  enc += "            <size column='[%s].%s' />\n" % (ds, esc(inst(size, T.get(size, "real"))))

    def shelf(fields):
        return " / ".join("[%s].%s" % (ds, esc(inst(f, T[f]))) for f in fields if f in T)
    rows_spec = shelf(rows_list)
    cols_spec = shelf(cols_list)

    enc_block = ("          <encodings>\n%s          </encodings>\n" % enc) if enc else ""
    return """  <worksheet name='%s'>
    <table>
      <view>
        <datasources>
          <datasource caption='%s' name='%s' />
        </datasources>
        <datasource-dependencies datasource='%s'>
%s
        </datasource-dependencies>
%s        <aggregation value='true' />
      </view>
      <style />
      <panes>
        <pane selection-relaxation-option='selection-relaxation-allow'>
          <view><breakdown value='auto' /></view>
          <mark class='%s' />
%s        </pane>
      </panes>
      <rows>%s</rows>
      <cols>%s</cols>
    </table>
    <simple-id uuid='{%s}' />
  </worksheet>""" % (esc(name), esc(ds), ds, ds,
                     "\n".join(deps), fx, mark, enc_block, rows_spec, cols_spec,
                     _uuid(name))

# ── dashboard XML ───────────────────────────────────────────────────
def dashboard(name, sheets, cols=2, w=1400, h=900):
    """Lay sheets out on a simple grid in Tableau's 100000-unit zone space."""
    n = len(sheets)
    rows_n = (n + cols - 1) // cols
    zw, zh = 100000 // cols, 100000 // rows_n
    zones = ""
    zid = 10
    for i, s in enumerate(sheets):
        r, c = divmod(i, cols)
        zones += ("        <zone h='%d' id='%d' name='%s' w='%d' x='%d' y='%d'>"
                  "<layout-cache minheight='180' minwidth='160' type-h='scalable' type-w='scalable' />"
                  "<zone-style><format attr='border-color' value='#e0e5ea' />"
                  "<format attr='border-style' value='solid' />"
                  "<format attr='border-width' value='1' />"
                  "<format attr='margin' value='4' /></zone-style></zone>\n"
                  % (zh, zid, esc(s), zw, c * zw, r * zh))
        zid += 1
    return """  <dashboard enable-sort-zone-taborder='true' name='%s'>
    <style />
    <size maxheight='%d' maxwidth='%d' minheight='%d' minwidth='%d' sizing-mode='fixed' />
    <zones>
      <zone h='100000' id='1' type-v2='layout-basic' w='100000' x='0' y='0'>
%s      </zone>
    </zones>
    <simple-id uuid='{%s}' />
  </dashboard>""" % (esc(name), h, w, h, w, zones, _uuid("dash:" + name))

# ── assembly ────────────────────────────────────────────────────────
def build(twb_path, twbx_path, datasources, worksheets, dashboards):
    ds_xml, sheet_xml = [], []
    meta = {}
    for ds_name, filename, caption in datasources:
        hdr, types, xml = datasource(ds_name, filename, caption)
        meta[ds_name] = (hdr, types)
        ds_xml.append(xml)
    for spec in worksheets:
        ds = spec["ds"]
        hdr, types = meta[ds]
        sheet_xml.append(worksheet(spec["name"], ds, hdr, types,
                                   spec.get("rows"), spec.get("cols"),
                                   spec.get("mark", "Bar"), spec.get("color"),
                                   spec.get("label"), spec.get("size"),
                                   spec.get("filters"), spec.get("sort"),
                                   spec.get("title")))
    dash_xml = [dashboard(d["name"], d["sheets"], d.get("cols", 2),
                          d.get("w", 1400), d.get("h", 900)) for d in dashboards]

    # ── windows ───────────────────────────────────────────────────
    # Required. The schema content model is
    #   ((cards, viewpoint?) | (viewpoints, active, device-preview))
    # so a worksheet window carries <cards> and a dashboard window carries
    # <viewpoints> + <active>.
    win = []
    for spec in worksheets:
        win.append("""    <window class='worksheet' name='%s'>
      <cards>
        <edge name='left'>
          <strip size='160'>
            <card type='pages' />
            <card type='filters' />
            <card type='marks' />
          </strip>
        </edge>
        <edge name='top'>
          <strip size='2147483647'><card type='columns' /></strip>
          <strip size='2147483647'><card type='rows' /></strip>
          <strip size='31'><card type='title' /></strip>
        </edge>
      </cards>
      <simple-id uuid='{%s}' />
    </window>""" % (esc(spec["name"]), _uuid("win:" + spec["name"])))
    for d in dashboards:
        vps = "\n".join("        <viewpoint name='%s'><zoom type='entire-view' /></viewpoint>"
                        % esc(s) for s in d["sheets"])
        win.append("""    <window class='dashboard' name='%s'>
      <viewpoints>
%s
      </viewpoints>
      <active id='-1' />
      <simple-id uuid='{%s}' />
    </window>""" % (esc(d["name"]), vps, _uuid("dwin:" + d["name"])))
    windows_xml = "  <windows source-height='30'>\n" + "\n".join(win) + "\n  </windows>"

    xml = """<?xml version='1.0' encoding='utf-8' ?>
<workbook original-version='18.1' source-build='2026.2.1 (20262.26.0708.1337)' source-platform='mac' version='18.1' xmlns:user='http://www.tableausoftware.com/xml/user'>
  <document-format-change-manifest>
    <AccessibleZoneTabOrder />
    <AnimationOnByDefault />
    <AutoCreateAndUpdateDSDPhoneLayouts />
    <MarkAnimation />
    <ObjectModelEncapsulateLegacy />
    <ObjectModelTableType />
    <SchemaViewerObjectModel />
    <SetMembershipControl />
    <SheetIdentifierTracking />
    <WindowsPersistSimpleIdentifiers />
  </document-format-change-manifest>
  <preferences>
    <preference name='ui.encoding.shelf.height' value='24' />
    <preference name='ui.shelf.height' value='26' />
  </preferences>
  <datasources>
%s
  </datasources>
  <worksheets>
%s
  </worksheets>
  <dashboards>
%s
  </dashboards>
%s
</workbook>
""" % ("\n".join(ds_xml), "\n".join(sheet_xml), "\n".join(dash_xml), windows_xml)

    with open(twb_path, "w", encoding="utf-8") as f:
        f.write(xml)

    used_files = sorted({fn for _, fn, _ in datasources})
    with zipfile.ZipFile(twbx_path, "w", zipfile.ZIP_DEFLATED) as z:
        z.write(twb_path, os.path.basename(twb_path))
        for fn in used_files:
            z.write(os.path.join(DATA, fn), os.path.join("Data", fn))
    return xml, used_files
