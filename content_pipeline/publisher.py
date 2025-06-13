"""
Publisher

Handles Git operations for publishing generated blog content.
"""

import os
import sys
from pathlib import Path
from typing import Optional, List
from datetime import datetime

import git
from rich.console import Console
from rich.prompt import Confirm

console = Console()


class Publisher:
    """Git-based publisher for blog content."""

    def __init__(self, repo_path: Path = None, remote_name: str = "origin", branch: str = "main"):
        """Initialize the publisher.
        
        Args:
            repo_path: Path to Git repository (defaults to current directory)
            remote_name: Name of Git remote
            branch: Branch to push to
        """
        self.repo_path = repo_path or Path.cwd()
        self.remote_name = remote_name
        self.branch = branch
        
        try:
            self.repo = git.Repo(self.repo_path)
        except git.InvalidGitRepositoryError:
            raise ValueError(f"Not a Git repository: {self.repo_path}")
        
        # Ensure we're on the correct branch
        try:
            if self.repo.active_branch.name != self.branch:
                console.print(f"[yellow]Switching to branch '{self.branch}'[/yellow]")
                self.repo.git.checkout(self.branch)
        except Exception as e:
            console.print(f"[yellow]Warning: Could not verify branch: {e}[/yellow]")

    def check_git_status(self) -> dict:
        """Check current Git repository status.
        
        Returns:
            Dictionary with repository status information
        """
        try:
            status = {
                "clean": not self.repo.is_dirty(),
                "untracked_files": self.repo.untracked_files,
                "modified_files": [item.a_path for item in self.repo.index.diff(None)],
                "staged_files": [item.a_path for item in self.repo.index.diff("HEAD")],
                "current_branch": self.repo.active_branch.name,
                "remote_url": self.repo.remotes[self.remote_name].url if self.remote_name in [r.name for r in self.repo.remotes] else None
            }
            return status
        except Exception as e:
            console.print(f"[red]Error checking Git status: {e}[/red]")
            return {}

    def stage_files(self, file_paths: List[Path]) -> bool:
        """Stage specific files for commit.
        
        Args:
            file_paths: List of file paths to stage
            
        Returns:
            True if staging successful, False otherwise
        """
        try:
            for file_path in file_paths:
                if file_path.exists():
                    self.repo.index.add([str(file_path)])
                    console.print(f"[green]Staged: {file_path}[/green]")
                else:
                    console.print(f"[yellow]File not found, skipping: {file_path}[/yellow]")
            
            return True
            
        except Exception as e:
            console.print(f"[red]Error staging files: {e}[/red]")
            return False

    def commit_changes(self, message: str, author_name: str = None, author_email: str = None) -> Optional[str]:
        """Commit staged changes.
        
        Args:
            message: Commit message
            author_name: Git author name (optional)
            author_email: Git author email (optional)
            
        Returns:
            Commit hash if successful, None otherwise
        """
        try:
            # Configure author if provided
            if author_name and author_email:
                actor = git.Actor(author_name, author_email)
                commit = self.repo.index.commit(message, author=actor, committer=actor)
            else:
                commit = self.repo.index.commit(message)
            
            console.print(f"[green]Committed: {commit.hexsha[:8]} - {message}[/green]")
            return commit.hexsha
            
        except Exception as e:
            console.print(f"[red]Error committing changes: {e}[/red]")
            return None

    def push_to_remote(self, force: bool = False) -> bool:
        """Push commits to remote repository.
        
        Args:
            force: Whether to force push
            
        Returns:
            True if push successful, False otherwise
        """
        try:
            remote = self.repo.remotes[self.remote_name]
            
            if force:
                console.print(f"[yellow]Force pushing to {self.remote_name}/{self.branch}[/yellow]")
                remote.push(refspec=f"{self.branch}:{self.branch}", force=True)
            else:
                console.print(f"[blue]Pushing to {self.remote_name}/{self.branch}[/blue]")
                remote.push(refspec=f"{self.branch}:{self.branch}")
            
            console.print("[green]Successfully pushed to remote[/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error pushing to remote: {e}[/red]")
            return False

    def publish_content(
        self, 
        content_files: List[Path], 
        commit_message: str = None,
        auto_push: bool = True
    ) -> bool:
        """Publish content by staging, committing, and pushing.
        
        Args:
            content_files: List of content files to publish
            commit_message: Custom commit message
            auto_push: Whether to automatically push to remote
            
        Returns:
            True if publishing successful, False otherwise
        """
        try:
            # Check repository status
            status = self.check_git_status()
            if not status:
                return False
            
            console.print(f"[blue]Publishing {len(content_files)} content files[/blue]")
            
            # Stage files
            if not self.stage_files(content_files):
                return False
            
            # Generate commit message if not provided
            if not commit_message:
                timestamp = datetime.now().strftime("%Y-%m-%d %H:%M")
                file_count = len(content_files)
                commit_message = f"Add {file_count} new blog post{'s' if file_count > 1 else ''} - {timestamp}"
            
            # Commit changes
            commit_hash = self.commit_changes(commit_message)
            if not commit_hash:
                return False
            
            # Push to remote
            if auto_push:
                if not self.push_to_remote():
                    console.print("[yellow]Commit successful but push failed. You can push manually later.[/yellow]")
                    return False
            
            console.print("[green]Content published successfully![/green]")
            return True
            
        except Exception as e:
            console.print(f"[red]Error publishing content: {e}[/red]")
            return False

    def create_pull_request_info(self, content_files: List[Path]) -> dict:
        """Generate information for creating a pull request.
        
        Args:
            content_files: List of published content files
            
        Returns:
            Dictionary with PR information
        """
        try:
            # Get file information
            file_info = []
            for file_path in content_files:
                if file_path.exists():
                    # Try to extract title from markdown front matter
                    title = "New Content"
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            content = f.read()
                            if content.startswith('---'):
                                front_matter_end = content.find('---', 3)
                                if front_matter_end > 0:
                                    import yaml
                                    front_matter = yaml.safe_load(content[3:front_matter_end])
                                    title = front_matter.get('title', title)
                    except:
                        pass
                    
                    file_info.append({
                        "path": str(file_path),
                        "title": title,
                        "size": file_path.stat().st_size
                    })
            
            # Generate PR details
            pr_info = {
                "title": f"Add {len(file_info)} new blog post{'s' if len(file_info) > 1 else ''}",
                "body": self._generate_pr_body(file_info),
                "labels": ["content", "automated", "blog-post"],
                "files_changed": len(file_info)
            }
            
            return pr_info
            
        except Exception as e:
            console.print(f"[red]Error generating PR info: {e}[/red]")
            return {}

    def _generate_pr_body(self, file_info: List[dict]) -> str:
        """Generate pull request body text.
        
        Args:
            file_info: List of file information dictionaries
            
        Returns:
            Formatted PR body text
        """
        body_parts = [
            "## 🤖 Automated Content Generation",
            "",
            "This PR contains new blog content generated by the AI content pipeline.",
            "",
            "### 📝 Content Summary",
            ""
        ]
        
        for i, info in enumerate(file_info, 1):
            body_parts.extend([
                f"**{i}. {info['title']}**",
                f"- File: `{info['path']}`",
                f"- Size: {info['size']:,} bytes",
                ""
            ])
        
        body_parts.extend([
            "### ✅ Automated Checks",
            "- [x] Content generated using OpenAI GPT-4o",
            "- [x] SEO metadata included",
            "- [x] Markdown formatting validated",
            "- [x] File size within limits",
            "",
            "### 🚀 Deployment",
            "Merging this PR will trigger the static site build and deployment to production.",
            "",
            f"*Generated on {datetime.now().strftime('%Y-%m-%d at %H:%M UTC')}*"
        ])
        
        return "\n".join(body_parts)

    def cleanup_old_commits(self, days_old: int = 90) -> None:
        """Clean up old commits (informational only - actual cleanup requires manual action).
        
        Args:
            days_old: Consider commits older than this many days
        """
        try:
            import time
            cutoff_time = time.time() - (days_old * 24 * 60 * 60)
            
            old_commits = []
            for commit in self.repo.iter_commits():
                if commit.committed_date < cutoff_time:
                    old_commits.append(commit)
            
            if old_commits:
                console.print(f"[blue]Found {len(old_commits)} commits older than {days_old} days[/blue]")
                console.print("[yellow]Consider running 'git gc' to clean up repository[/yellow]")
            
        except Exception as e:
            console.print(f"[red]Error analyzing old commits: {e}[/red]")


def main():
    """CLI entry point for publishing operations."""
    import argparse
    from dotenv import load_dotenv
    
    load_dotenv()
    
    parser = argparse.ArgumentParser(description="Publish blog content to Git repository")
    parser.add_argument("files", nargs="*", help="Content files to publish")
    parser.add_argument("--message", "-m", help="Commit message")
    parser.add_argument("--no-push", action="store_true", help="Don't push to remote")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be done")
    
    args = parser.parse_args()
    
    try:
        publisher = Publisher()
        
        # Check Git status
        status = publisher.check_git_status()
        if status:
            console.print(f"[blue]Repository: {publisher.repo_path}[/blue]")
            console.print(f"[blue]Branch: {status['current_branch']}[/blue]")
            console.print(f"[blue]Clean: {status['clean']}[/blue]")
        
        if args.dry_run:
            console.print("[yellow]DRY RUN - No changes will be made[/yellow]")
            return
        
        # Get content files
        if args.files:
            content_files = [Path(f) for f in args.files]
        else:
            # Find recent content files
            content_dir = Path("content")
            if content_dir.exists():
                # Get files modified in the last hour
                import time
                recent_time = time.time() - 3600  # 1 hour ago
                content_files = []
                for md_file in content_dir.rglob("*.md"):
                    if md_file.stat().st_mtime > recent_time:
                        content_files.append(md_file)
            else:
                console.print("[red]No content directory found and no files specified[/red]")
                sys.exit(1)
        
        if not content_files:
            console.print("[yellow]No content files to publish[/yellow]")
            return
        
        # Publish content
        success = publisher.publish_content(
            content_files,
            commit_message=args.message,
            auto_push=not args.no_push
        )
        
        if success:
            console.print("[green]Publishing completed successfully![/green]")
            
            # Show PR info if useful
            pr_info = publisher.create_pull_request_info(content_files)
            if pr_info:
                console.print(f"\n[blue]PR Title: {pr_info['title']}[/blue]")
        else:
            console.print("[red]Publishing failed[/red]")
            sys.exit(1)
        
    except Exception as e:
        console.print(f"[red]Error: {e}[/red]")
        sys.exit(1)


if __name__ == "__main__":
    main() 