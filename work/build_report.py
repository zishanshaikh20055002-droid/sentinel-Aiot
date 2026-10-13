from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.section import WD_SECTION

OUT = r"C:\Users\ZISHAN\Documents\Codex\2026-10-13\develop-a-privacy-aware-intelligent-smart-3\outputs\Sentinel_AIoT_Technical_Report.docx"
doc=Document(); sec=doc.sections[0]; sec.top_margin=Inches(.75); sec.bottom_margin=Inches(.72); sec.left_margin=Inches(.78); sec.right_margin=Inches(.78)
styles=doc.styles; styles['Normal'].font.name='Aptos'; styles['Normal'].font.size=Pt(10.2); styles['Normal'].paragraph_format.space_after=Pt(6)
for s,size in [('Title',26),('Heading 1',16),('Heading 2',12)]:
    st=styles[s]; st.font.name='Aptos'; st.font.size=Pt(size); st.font.color.rgb=RGBColor(0,0,0)
    st.font.bold=True

def shade(cell, fill):
    tcPr=cell._tc.get_or_add_tcPr(); shd=OxmlElement('w:shd'); shd.set(qn('w:fill'),fill); tcPr.append(shd)
def borders(table):
    tblPr=table._tbl.tblPr; e=OxmlElement('w:tblBorders')
    for n in ('top','left','bottom','right','insideH','insideV'):
        x=OxmlElement('w:'+n); x.set(qn('w:val'),'single'); x.set(qn('w:sz'),'4'); x.set(qn('w:color'),'D9D9D9'); e.append(x)
    tblPr.append(e)
def table(headers, rows, widths=None):
    t=doc.add_table(rows=1, cols=len(headers)); t.alignment=WD_TABLE_ALIGNMENT.CENTER; t.style='Table Grid'; borders(t)
    for i,h in enumerate(headers):
        c=t.rows[0].cells[i]; c.text=h; shade(c,'163A4A'); c.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
        for r in c.paragraphs[0].runs:r.font.bold=True;r.font.color.rgb=RGBColor(255,255,255)
        if widths:c.width=Inches(widths[i])
    for ri,row in enumerate(rows):
        cells=t.add_row().cells
        for i,v in enumerate(row):
            cells[i].text=str(v); cells[i].vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
            if ri%2==1: shade(cells[i],'EEF6F8')
            if widths:cells[i].width=Inches(widths[i])
    doc.add_paragraph('')
    return t
def p(text, boldlead=None):
    para=doc.add_paragraph()
    if boldlead:
        r=para.add_run(boldlead);r.bold=True
    para.add_run(text)
    return para
def bullet(text): doc.add_paragraph(text, style='List Bullet')

title=doc.add_paragraph(style='Title'); title.alignment=WD_ALIGN_PARAGRAPH.CENTER; title.add_run('Privacy Aware Intelligent Smart IoT System')
sub=doc.add_paragraph();sub.alignment=WD_ALIGN_PARAGRAPH.CENTER;sub.add_run('Design and Implementation Technical Report').bold=True
doc.add_paragraph('Sentinel Edge Cloud is a demonstrator for AIoT-based environmental sensing. It combines secure telemetry ingestion, cloud data preprocessing, anomaly-oriented machine learning, and privacy-by-design controls. The system is designed to support safety decisions while collecting only data needed for the defined purpose.').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_paragraph('Project deliverable | Interactive demonstration and architecture report | 13 October 2026').alignment=WD_ALIGN_PARAGRAPH.CENTER
doc.add_page_break()

doc.add_heading('1 Executive Summary',1)
p('The implementation demonstrates an intelligent sensor platform that detects unusual environmental conditions and recommends an action while maintaining an explicit privacy boundary. Sensor messages are authenticated at the gateway, reduced to the minimum useful fields, pseudonymised, cleaned, and transformed into a model feature vector. The decision layer combines an anomaly score with a deterministic safety rule and retains human override.')
p('The companion web console uses synthetic telemetry and shows the full logical processing path. It is suitable for an academic demonstration or a prototype review, rather than a production claim.')
doc.add_heading('2 Scope and Requirements',1)
table(['Requirement','Implementation response','Evidence in demonstration'],[
['Continuous sensing','Temperature, humidity, and CO2 trend are represented as streaming telemetry.','Live signal chart and message counter'],
['Secure communication','Mutual device authentication and TLS 1.3 are modeled at the gateway boundary.','Verified channel indicator and processing trace'],
['Privacy protection','Pseudonyms, zone-level location, minimisation, retention, and role separation.','Privacy posture panel and control dialog'],
['Intelligent decisions','Isolation Forest style anomaly score combined with a policy threshold.','Decision card and advisory path'],
['Cloud preprocessing','Validation, missing-value handling, normalisation, rolling trend features.','Architecture flow and report pipeline']
],[1.3,3.15,2.1])

doc.add_heading('3 System Architecture',1)
p('The design separates the edge, transport, cloud preprocessing, intelligence, and decision layers. This separation prevents raw contextual information from being propagated unnecessarily and allows each control to be independently audited.')
table(['Layer','Responsibility','Privacy and security mechanism'],[
['Edge sensor','Reads local measurements and applies coarse threshold checks.','Device private key in protected storage; no user profile collected.'],
['Secure gateway','Authenticates device and validates message schema.','mTLS, certificate rotation, rate control, consent and purpose tag validation.'],
['Preprocessing service','Cleans, aggregates, normalises, and generates features.','Pseudonymous session ID; zone rather than exact coordinates; encrypted queue.'],
['ML inference','Scores deviation from learned normal operation.','Feature-only inference; signed model release; confidence and drift logging.'],
['Decision service','Maps risk to advisory or controlled action.','Least-privilege role, human override, tamper-evident event record.']
],[1.2,2.45,2.9])
doc.add_heading('4 Secure Communication Design',1)
p('A device begins with a factory or enrolled identity and authenticates to the gateway using a short-lived client certificate. The gateway terminates TLS 1.3, checks the certificate chain and revocation state, then accepts an MQTT message only for an authorised topic. Payload integrity is provided by the authenticated transport; replay resistance is strengthened through timestamps, nonces, and server-side sequence windows.')
bullet('Use distinct device, gateway, and service identities. Do not share a fleet-wide secret.')
bullet('Rotate certificates and signing keys; record key status without recording secret material.')
bullet('Reject malformed, stale, unauthorised, or rate-abusive messages before persistence.')

doc.add_page_break()
doc.add_heading('5 Cloud Data Preprocessing',1)
p('Cloud preprocessing converts incoming telemetry into a bounded, quality-controlled representation. The target record contains a pseudonymous device session, approved zone, timestamp bucket, selected sensor measures, quality flags, and derived trend features. Raw identifiers and high-precision location are intentionally excluded from the analytical store.')
table(['Stage','Operation','Output'],[
['Validation','Type, range, timestamp, authorisation, and duplicate checks.','Accepted or rejected message with reason code.'],
['Cleaning','Drop duplicates; flag implausible values; impute short gaps only.','Quality-labelled readings.'],
['Minimisation','Replace ID; reduce spatial accuracy; remove unneeded metadata.','Pseudonymous analytics record.'],
['Transformation','Scale values; compute rolling mean, slope, and variance.','Feature vector for inference.'],
['Retention','Expire raw packet quickly; retain aggregate only when justified.','24-hour default operational window.']
],[1.25,3.2,2.1])
doc.add_heading('6 Machine Learning and Decision Logic',1)
p('The prototype uses an unsupervised anomaly-detection pattern suitable when examples of faults are scarce. A baseline Isolation Forest is trained on vetted normal-operation features. At inference, a score between 0 and 1 expresses relative abnormality. The user-facing console defaults to normal operation below 0.72 and presents an operator advisory when the score crosses that threshold.')
p('The decision is deliberately not model-only. A policy engine first verifies data quality and then combines the score with hard safety rules. For example, a high CO2 trend can recommend increased fresh-air intake. A shutdown-grade action requires an explicit policy condition and a logged human approval in this prototype.')
table(['Metric','Target','Prototype evaluation approach'],[
['Detection recall','At least 0.85 for scripted abnormal patterns','Replay labelled synthetic scenarios.'],
['False alert rate','Less than 5 percent on normal stream','Hold-out normal-operation sequences.'],
['Inference latency','Below 500 ms after ingestion','Timestamp each pipeline stage.'],
['Privacy leakage','No direct identifier in feature store','Schema and log inspection.']
],[1.6,1.75,3.2])
doc.add_heading('7 Privacy and Governance',1)
p('Privacy is a system property rather than a display setting. The design limits collection to environmental values required for safety analytics. Device identifiers are pseudonymised before analytics storage, exact spatial information is converted to an approved zone, and retention is bounded. Access is role-based: operations staff can view current decisions, security staff can review authentication events, and model reviewers receive feature-level data only.')
bullet('Purpose limitation: each topic carries a permitted processing purpose and policy version.')
bullet('Data subject protection: avoid personal or behavioural data; do not use telemetry for secondary profiling.')
bullet('Auditability: record policy decision, model version, score, and operator override without storing secrets.')

doc.add_page_break()
doc.add_heading('8 Demonstration Guide',1)
p('Open the Sentinel AIoT Privacy Console. The initial screen presents the secure channel state, sensor signal, privacy score, model confidence, and current decision. Select Run secure ingestion to produce simulated accepted telemetry, update the signal, and append entries to the processing trace. The run may end in a normal decision or a review advisory so both operational states can be demonstrated. Select View privacy controls to inspect minimisation, encryption, access, and retention controls.')
table(['Demonstration step','Expected observation','Requirement covered'],[
['Initial view','Normal state, mTLS indicator, pseudonymisation posture.','Secure and private architecture'],
['Secure ingestion','Counter and sensor signal advance; trace records transformations.','Cloud data preprocessing'],
['Advisory state','When triggered, fresh-air advisory and review state appear.','Intelligent decision-making'],
['Privacy view','Policy controls and reduced data representation are visible.','Built-in privacy mechanisms']
],[1.5,3.0,2.05])
doc.add_heading('9 Test Plan and Results',1)
table(['Test case','Expected result','Demonstration result'],[
['Untrusted device','Gateway rejects message before storage.','Represented by verification control; requires backend test in production.'],
['Out-of-range value','Quality flag prevents direct model use.','Specified preprocessing control.'],
['Normal telemetry','Low anomaly score; maintain normal ventilation.','Implemented in interactive console.'],
['Rising anomaly','Score exceeds threshold; operator advisory is raised.','Implemented in interactive console.'],
['Privacy inspection','No direct ID or exact location shown.','Implemented in privacy panel.']
],[1.5,3.0,2.05])
doc.add_heading('10 Limitations and Next Steps',1)
p('The delivered application is a front-end demonstrator with simulated events. A production implementation should add a device registry, managed PKI, backend message broker, encrypted database, key management service, consent register, model training pipeline, continuous drift monitoring, penetration testing, and an organisation-specific data protection impact assessment. Thresholds must be calibrated with domain experts before controlling physical equipment.')
doc.add_heading('11 Conclusion',1)
p('Sentinel Edge Cloud demonstrates a feasible privacy-aware AIoT pattern: authenticate and minimise at the boundary, preprocess only authorised attributes, score bounded features, and keep consequential decisions observable and overrideable. The design makes the trade-off explicit: meaningful operational intelligence can be delivered without retaining unnecessary identity or precision data.')

footer=doc.sections[0].footer.paragraphs[0]; footer.alignment=WD_ALIGN_PARAGRAPH.CENTER; footer.add_run('Sentinel AIoT Technical Report | Privacy aware intelligent sensing')
doc.core_properties.title='Privacy Aware Intelligent Smart IoT System'
doc.core_properties.author='Sentinel AIoT Project'
doc.save(OUT)
print(OUT)
