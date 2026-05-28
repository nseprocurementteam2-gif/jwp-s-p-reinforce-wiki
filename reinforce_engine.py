import os
import json
import uuid
import datetime
from pathlib import Path
from typing import List, Dict, Any
import subprocess
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich import print

console = Console()

class PReinforceEngine:
    def __init__(self, root_path: str):
        self.root = Path(root_path)
        self.raw_dir = self.root / "00_Raw"
        self.wiki_dir = self.root / "10_Wiki"
        self.meta_dir = self.root / "20_Meta"
        self.policy_path = self.meta_dir / "Policy.md"
        self.graph_path = self.meta_dir / "Graph.json"
        self.index_path = self.meta_dir / "Index.md"
        
        self.ensure_dirs()

    def ensure_dirs(self):
        for d in [self.raw_dir, self.wiki_dir, self.meta_dir]:
            d.mkdir(parents=True, exist_ok=True)
        for cat in ["Projects", "Topics", "Decisions", "Skills"]:
            (self.wiki_dir / cat).mkdir(parents=True, exist_ok=True)

    def load_graph(self) -> Dict:
        if self.graph_path.exists():
            with open(self.graph_path, "r", encoding="utf-8") as f:
                return json.load(f)
        return {"nodes": [], "edges": [], "metadata": {}}

    def save_graph(self, graph: Dict):
        graph["metadata"]["last_updated"] = datetime.datetime.now().strftime("%Y-%m-%d")
        graph["metadata"]["total_nodes"] = len(graph["nodes"])
        graph["metadata"]["total_edges"] = len(graph["edges"])
        with open(self.graph_path, "w", encoding="utf-8") as f:
            json.dump(graph, f, indent=2, ensure_ascii=False)

    def get_raw_files(self) -> List[Path]:
        files = []
        for day_dir in self.raw_dir.iterdir():
            if day_dir.is_dir():
                files.extend(list(day_dir.glob("*.md")) + list(day_dir.glob("*.txt")))
        return files

    def categorize_logic(self, content: str) -> Dict[str, Any]:
        """
        [TODO] 실제 LLM API 연동부. 
        현재는 사용자가 이 스크립트를 실행할 때 LLM의 역할을 대신하거나 
        기본적인 키워드 매칭으로 시뮬레이션합니다.
        """
        # 임시 로직: 내용에 따라 분류 제안
        category = "Topics"
        if "Project" in content or "프로젝트" in content:
            category = "Projects"
        elif "Decision" in content or "결정" in content:
            category = "Decisions"
        elif "Skill" in content or "프롬프트" in content:
            category = "Skills"
            
        return {
            "category": f"10_Wiki/{category}",
            "confidence_score": 0.9,
            "tags": ["auto-classified"],
            "summary": "자동으로 분류된 지식입니다."
        }

    def create_wiki_doc(self, raw_file: Path, metadata: Dict):
        with open(raw_file, "r", encoding="utf-8") as f:
            raw_content = f.read()

        doc_id = str(uuid.uuid4())
        title = raw_file.stem
        today = datetime.datetime.now().strftime("%Y-%m-%d")
        
        wiki_path = self.root / metadata["category"] / f"{title}.md"
        
        template = f"""---
id: {doc_id}
category: "[[{metadata['category']}]]"
confidence_score: {metadata['confidence_score']}
tags: {metadata['tags']}
last_reinforced: {today}
github_commit: "pending"
---

# [[{title}]]

## 📌 한 줄 통찰 (The Karpathy Summary)
> {metadata['summary']}

## 📖 구조화된 지식 (Synthesized Content)
{raw_content}

## ⚠️ 모순 및 업데이트 (Contradictions & RL Update)
- **과거 데이터와의 충돌:** 없음.
- **정책 변화:** 초기 분류 기준 적용.

## 🔗 지식 연결 (Graph)
- **Parent:** [[{metadata['category']}]]
- **Related:** []
- **Raw Source:** [[00_Raw/{raw_file.parent.name}/{raw_file.name}]]
"""
        with open(wiki_path, "w", encoding="utf-8") as f:
            f.write(template)
            
        return wiki_path, doc_id

    def update_graph(self, doc_id: str, title: str, category: str):
        graph = self.load_graph()
        # 노드 중복 체크
        if not any(n["id"] == doc_id for n in graph["nodes"]):
            graph["nodes"].append({
                "id": doc_id,
                "label": title,
                "category": category,
                "last_updated": datetime.datetime.now().strftime("%Y-%m-%d")
            })
        self.save_graph(graph)
        self.update_index()

    def update_index(self):
        # Wiki 폴더 내의 파일들을 스캔하여 Index.md 갱신
        docs = []
        for cat in ["Projects", "Topics", "Decisions", "Skills"]:
            path = self.wiki_dir / cat
            for f in path.glob("*.md"):
                docs.append(f"- [{f.stem}](file:///{f.as_posix()}) ({cat})")
        
        content = f"""# P-Reinforce Knowledge Index

환영합니다. P-Reinforce 엔진이 구축한 지식의 입구입니다.

## 🗺️ 지식 지도 (Map of Knowledge)
- [🛠️ Projects](file:///{ (self.wiki_dir / 'Projects').as_posix() })
- [💡 Topics](file:///{ (self.wiki_dir / 'Topics').as_posix() })
- [⚖️ Decisions](file:///{ (self.wiki_dir / 'Decisions').as_posix() })
- [🚀 Skills](file:///{ (self.wiki_dir / 'Skills').as_posix() })

## 📂 전체 지식 목록
{chr(10).join(docs) if docs else "아직 등록된 지식이 없습니다."}

## 📊 시스템 현황
- **마지막 강화(Reinforced):** {datetime.datetime.now().strftime("%Y-%m-%d")}
- **총 문서 수:** {len(docs)}
- **그래프 연결 밀도:** 0%

---
*Created and maintained by P-Reinforce Architect.*
"""
        with open(self.index_path, "w", encoding="utf-8") as f:
            f.write(content)

    def reinforce(self):
        console.print(Panel("[bold green]P-Reinforce Engine Starting...[/bold green]"))
        raw_files = self.get_raw_files()
        
        if not raw_files:
            console.print("[yellow]00_Raw 폴더에 처리할 지식이 없습니다.[/yellow]")
            return

        table = Table(title="처리 대기 중인 원시 데이터")
        table.add_column("날짜", style="cyan")
        table.add_column("파일명", style="magenta")
        
        for f in raw_files:
            table.add_row(f.parent.name, f.name)
        
        console.print(table)
        
        for f in raw_files:
            console.print(f"\n[bold]Reinforcing: {f.name}...[/bold]")
            # 1. 분류 및 메타데이터 추출
            with open(f, "r", encoding="utf-8") as file:
                content = file.read()
            
            meta = self.categorize_logic(content)
            
            # 2. 위키 문서 생성
            wiki_file, doc_id = self.create_wiki_doc(f, meta)
            console.print(f"  [green]+[/green] 위키 생성 완료: {wiki_file.relative_to(self.root)}")
            
            # 3. 그래프 업데이트
            self.update_graph(doc_id, f.stem, meta["category"])
            console.print(f"  [green]+[/green] 지식 그래프 업데이트 완료")
            
        console.print("\n[bold green]모든 지식 강화 완료![/bold green]")

    def git_sync(self, message: str):
        try:
            subprocess.run(["git", "add", "."], cwd=self.root, check=True)
            subprocess.run(["git", "commit", "-m", f"[P-Reinforce] {message}"], cwd=self.root, check=True)
            console.print(f"[bold blue]Git Sync:[/bold blue] {message}")
        except Exception as e:
            console.print(f"[red]Git Sync 도중 오류 발생: {e}[/red]")

if __name__ == "__main__":
    engine = PReinforceEngine(os.getcwd())
    engine.reinforce()
    # engine.git_sync("지식 구조화 및 동기화 수행")
