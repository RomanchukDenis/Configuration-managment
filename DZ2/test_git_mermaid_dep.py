import subprocess

import pytest
from git_mermaid_dep import load_config, get_commits_from_repo, generate_mermaid_graph
import os

def test_load_config(tmpdir):
    config_content = "repository_path: /test/repo\nvisualization_program_path: /test/mermaid"
    config_file = tmpdir.join("config.yaml")
    config_file.write(config_content)

    config = load_config(config_file)
    assert config["repository_path"] == "/test/repo"
    assert config["visualization_program_path"] == "/test/mermaid"

def test_get_commits_from_repo(mocker):
    mocker.patch("subprocess.run", return_value=subprocess.CompletedProcess(
        args=[], returncode=0, stdout="hash1;;John Doe;2024-06-01\nhash2;hash1;Jane Smith;2024-06-02"
    ))
    commits = get_commits_from_repo("/test/repo")
    assert "hash1" in commits
    assert commits["hash1"]["author"] == "John Doe"

def test_generate_mermaid_graph(tmpdir):
    commits = {
        "hash1": {"parents": [], "author": "John Doe", "date": "2024-06-01"},
        "hash2": {"parents": ["hash1"], "author": "Jane Smith", "date": "2024-06-02"}
    }
    output_file = tmpdir.join("graph.mermaid")
    generate_mermaid_graph(commits, output_file)
    content = output_file.read()
    assert "hash1" in content
    assert "hash2" in content
    assert "hash1 --> hash2" in content  # Исправлено направление
