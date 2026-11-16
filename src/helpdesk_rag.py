from __future__ import annotations
import argparse, pickle
from pathlib import Path
import numpy as np
from pypdf import PdfReader
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

def read_doc(path: Path) -> str:
    if path.suffix.lower() == ".pdf":
        return "\n".join((p.extract_text() or "") for p in PdfReader(str(path)).pages)
    return path.read_text(encoding="utf-8", errors="replace")

def chunk(text: str, size=850, overlap=150):
    text = " ".join(text.split())
    out, i = [], 0
    while i < len(text):
        out.append(text[i:i+size])
        i += max(1, size-overlap)
    return [x for x in out if x.strip()]

def collect(folder):
    items=[]
    for p in Path(folder).rglob("*"):
        if p.is_file() and p.suffix.lower() in {".pdf",".md",".txt"}:
            for n,c in enumerate(chunk(read_doc(p))):
                items.append({"source":str(p),"chunk":n,"text":c})
    return items

def build(folder,index_dir):
    docs=collect(folder)
    if not docs: raise ValueError("No supported documents found.")
    vec=TfidfVectorizer(stop_words="english",ngram_range=(1,2))
    matrix=vec.fit_transform([d["text"] for d in docs])
    out=Path(index_dir); out.mkdir(parents=True,exist_ok=True)
    with open(out/"index.pkl","wb") as f:
        pickle.dump({"docs":docs,"vectorizer":vec,"matrix":matrix},f)
    print(f"Indexed {len(docs)} passages.")

def ask(index_dir,question,top_k=4,min_score=0.05):
    with open(Path(index_dir)/"index.pkl","rb") as f:
        data=pickle.load(f)
    q=data["vectorizer"].transform([question])
    scores=cosine_similarity(q,data["matrix"])[0]
    order=np.argsort(scores)[::-1][:top_k]
    hits=[]
    for i in order:
        if float(scores[i]) < min_score: continue
        d=data["docs"][int(i)]
        hits.append({"score":float(scores[i]),**d})
    if not hits:
        print("No sufficiently relevant approved documentation was found.")
        return
    print("Evidence-backed response:")
    for n,h in enumerate(hits,1):
        print(f"\n[{n}] {h['text']}\nSource: {h['source']} (chunk {h['chunk']}, score {h['score']:.3f})")

def main():
    ap=argparse.ArgumentParser(); sub=ap.add_subparsers(dest="cmd",required=True)
    a=sub.add_parser("index"); a.add_argument("folder"); a.add_argument("--index-dir",default="index")
    q=sub.add_parser("ask"); q.add_argument("index_dir"); q.add_argument("question"); q.add_argument("--top-k",type=int,default=4)
    x=ap.parse_args()
    build(x.folder,x.index_dir) if x.cmd=="index" else ask(x.index_dir,x.question,x.top_k)
if __name__=="__main__": main()
