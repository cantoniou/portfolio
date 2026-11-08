// Word version of the one-page CV. Same content as the PDF (reads data/cv.yaml via build.py).
// Usage (via build.py): node docx/onepager.js <data.json> <out.docx>
const fs = require("fs");
const path = require("path");
const d = require("docx");
const data = JSON.parse(fs.readFileSync(process.argv[2], "utf8"));
const out = process.argv[3];
const ROOT = path.join(__dirname, "..");

const ACCENT = "0065BD", INK = "1B1F24", MUTED = "5B6670", PANEL = "F2F5F9";
const FONT = "Calibri";
const MAIN = 18, SIDE = 17, SMALL = 15;          // half-points
const mm = (x) => Math.round(x * 56.6929);         // mm -> twips
const NB = { style: d.BorderStyle.NONE, size: 0, color: "FFFFFF" };
const NOBORDERS = { top: NB, bottom: NB, left: NB, right: NB, insideHorizontal: NB, insideVertical: NB };

// "**bold** and *italic*" -> TextRuns
function runs(text, o = {}) {
  const parts = String(text).split(/(\*\*[^*]+\*\*|\*[^*]+\*)/).filter(Boolean);
  return parts.map((p) => {
    let bold = o.bold, italics = o.italics, t = p;
    if (p.startsWith("**")) { bold = true; t = p.slice(2, -2); }
    else if (p.startsWith("*")) { italics = true; t = p.slice(1, -1); }
    return new d.TextRun({ text: t, bold, italics, font: FONT, size: o.size || MAIN, color: o.color || INK });
  });
}
const P = (children, o = {}) => new d.Paragraph({ children, spacing: { before: o.before || 0, after: o.after || 0, line: o.line || 252, lineRule: d.LineRuleType.AUTO }, alignment: o.align, border: o.border, bullet: o.bullet, indent: o.indent, tabStops: o.tabStops, keepLines: true });
const link = (label, url, size) => new d.ExternalHyperlink({ link: url, children: [new d.TextRun({ text: label, font: FONT, size, color: ACCENT })] });

function mainHead(t, first) {
  return P(runs(t.toUpperCase(), { bold: true, color: ACCENT, size: 17 }),
    { before: first ? 0 : 150, after: 60, border: { bottom: { style: d.BorderStyle.SINGLE, size: 6, color: ACCENT, space: 1 } } });
}
function sideHead(t, first) { return P(runs(t.toUpperCase(), { bold: true, color: ACCENT, size: 16 }), { before: first ? 60 : 150, after: 40 }); }
const bullet = (children) => P([new d.TextRun({ text: "•\t", font: FONT, size: MAIN, color: ACCENT }), ...children], { after: 25, indent: { left: 170, hanging: 170 }, tabStops: [{ type: d.TabStopType.LEFT, position: 170 }] });

const p = data.person;

// ---------- header ----------
const photo = new d.ImageRun({ type: "png", data: fs.readFileSync(path.join(ROOT, p.photo)), transformation: { width: 84, height: 84 } });
const header = new d.Table({
  width: { size: 100, type: d.WidthType.PERCENTAGE }, borders: NOBORDERS,
  columnWidths: [mm(25), mm(105), mm(56)],
  rows: [new d.TableRow({ children: [
    new d.TableCell({ verticalAlign: d.VerticalAlign.CENTER, children: [P([photo])] }),
    new d.TableCell({ verticalAlign: d.VerticalAlign.CENTER, children: [
      P(runs(p.title, { bold: true, size: 20 })),
      P(runs(p.name, { bold: true, size: 46, color: ACCENT }), { after: 40 }),
      P(runs(p.position, { bold: true, size: 19 })),
      ...p.affiliation.slice(1).map((a) => P(runs(a, { color: MUTED, size: 18 }))),
    ] }),
    new d.TableCell({ verticalAlign: d.VerticalAlign.CENTER, children: [
      P([link(p.email, "mailto:" + p.email, SIDE)], { align: d.AlignmentType.RIGHT, line: 260 }),
      ...p.links.map((l) => P([link(l.label, l.url, SIDE)], { align: d.AlignmentType.RIGHT, line: 260 })),
      P([...runs("ORCID ", { color: MUTED, size: SIDE }), link(p.ids.orcid, "https://orcid.org/" + p.ids.orcid, SIDE)], { align: d.AlignmentType.RIGHT, line: 260 }),
    ] }),
  ] })],
});
const rule = P([], { after: 80, border: { bottom: { style: d.BorderStyle.SINGLE, size: 18, color: ACCENT, space: 1 } } });

// ---------- left panel ----------
const left = [sideHead("In numbers", true)];
for (const m of data.metrics) {
  left.push(P(runs(m.value, { bold: true, color: ACCENT, size: 28 }), { line: 230 }));
  left.push(P(runs(m.label, { color: MUTED, size: SMALL }), { after: 70 }));
}
left.push(P(runs(data.metrics_source_label + ".", { color: MUTED, size: 12 }), { after: 40 }));
left.push(sideHead("Education"));
data.education.forEach((e) => { left.push(P(runs(e.short, { bold: true, size: SIDE }))); left.push(P(runs(`${e.institution}, ${e.end}`, { size: SIDE }), { after: 50 })); });
left.push(sideHead("Research interests"));
data.research_interests.short.forEach((r) => left.push(P(runs(r, { size: SIDE }), { after: 10 })));
left.push(sideHead("Languages"));
data.languages.forEach((l) => left.push(P(runs(`${l.lang} (${l.level})`, { size: SIDE }), { after: 10 })));
left.push(sideHead("Honours (selected)"));
data.honours.short.forEach((h) => left.push(P(runs(h, { size: SIDE }), { after: 20 })));
left.push(sideHead("Links"));
left.push(P([...runs("Google Scholar ", { size: SIDE }), link(p.ids.scholar, "https://scholar.google.com/citations?user=" + p.ids.scholar, SIDE)]));
left.push(P([...runs("Scopus ", { size: SIDE }), link(p.ids.scopus, "https://www.scopus.com/authid/detail.uri?authorId=" + p.ids.scopus, SIDE)]));
if (p.ids.linkedin) left.push(P([...runs("LinkedIn ", { size: SIDE }), link(p.ids.linkedin, "https://www.linkedin.com/in/" + p.ids.linkedin + "/", SIDE)]));
left.push(P([...runs("ORCID ", { size: SIDE }), link(p.ids.orcid, "https://orcid.org/" + p.ids.orcid, SIDE)]));

// ---------- main column ----------
const main = [mainHead("Profile", true), P(runs(data.profile_short))];
main.push(mainHead("Career"));
for (const c of data.career.filter((c) => c.onepager)) {
  main.push(P([...runs(c.onepager.title, { bold: true }), new d.TextRun({ text: "\t" + c.onepager.when, font: FONT, size: MAIN, color: MUTED })],
    { tabStops: [{ type: d.TabStopType.RIGHT, position: mm(122) }] }));
  main.push(P(runs(c.onepager.where, { color: MUTED }), { after: 50 }));
}
main.push(mainHead(data.projects_heading || "Funded projects"));
for (const [k, label] of [["eu", "EU"], ["dfg", "DFG"], ["national", "National"]]) {
  const ch = runs(label + ": ", { bold: true });
  data.projects[k].forEach((pr, i) => {
    ch.push(new d.TextRun({ text: pr.name, font: FONT, size: MAIN, color: pr.status === "closed" ? MUTED : INK, italics: pr.status === "closed" }));
    if (i < data.projects[k].length - 1) ch.push(new d.TextRun({ text: ", ", font: FONT, size: MAIN, color: INK }));
  });
  main.push(bullet(ch));
}
main.push(P(runs("Active projects in regular type, completed in *grey italics*.", { color: MUTED, size: SMALL }), { before: 20 }));
main.push(mainHead("Selected publications"));
data.publications_selected.forEach((x) => main.push(bullet(runs(x))));
main.push(mainHead("Teaching and supervision"));
main.push(bullet(runs(data.supervision.onepager.charAt(0).toUpperCase() + data.supervision.onepager.slice(1))));
main.push(bullet(runs(data.teaching.onepager)));
main.push(mainHead("Service and leadership"));
data.service.onepager.forEach((x) => main.push(bullet(runs(x))));

const body = new d.Table({
  width: { size: 100, type: d.WidthType.PERCENTAGE }, borders: NOBORDERS,
  columnWidths: [mm(53), mm(4), mm(129)],
  rows: [new d.TableRow({ children: [
    new d.TableCell({ shading: { type: d.ShadingType.CLEAR, fill: PANEL, color: "auto" }, margins: { top: mm(1.5), bottom: mm(1.5), left: mm(2), right: mm(2) }, children: left }),
    new d.TableCell({ children: [P([])] }),
    new d.TableCell({ children: main }),
  ] })],
});
const footer = P([...runs(`${data.metrics_source_label}. Other figures as of ${data.metrics_as_of}. Full publication list: `, { color: MUTED, size: SMALL }), link("orcid.org/" + p.ids.orcid, "https://orcid.org/" + p.ids.orcid, SMALL)], { before: 120 });

const doc = new d.Document({
  creator: "CV master", title: `CV ${p.name}`,
  styles: { default: { document: { run: { font: FONT, size: MAIN, color: INK } } } },
  numbering: undefined,
  sections: [{ properties: { page: { size: { width: mm(210), height: mm(297) }, margin: { top: mm(10), bottom: mm(9), left: mm(12), right: mm(12) } } },
    children: [header, rule, body, footer] }],
});
d.Packer.toBuffer(doc).then((b) => fs.writeFileSync(out, b));
