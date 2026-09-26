#!/usr/bin/env python3
import pytest
import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from company_commander import CompanyCommander

def test_company_commander_initialization():
    commander = CompanyCommander()
    assert os.path.exists(commander.root_dir)

def test_daily_command_brief_structure():
    commander = CompanyCommander()
    brief = commander.get_daily_command_brief()
    assert "DATE" in brief
    assert "COMPANY STAGE" in brief
    assert "CASH" in brief
    assert "REVENUE" in brief
    assert len(brief["TOP_3_ACTIONS"]) == 3
    assert "ONE_THING_TO_STOP" in brief
    assert "ONE_THING_TO_WATCH" in brief

def test_compress_directive():
    commander = CompanyCommander()
    c = commander.compress_directive()
    assert "WHAT_MATTERS" in c
    assert "EVIDENCE" in c
    assert "DECISION" in c
    assert len(c["NEXT_3_ACTIONS"]) == 3

def test_prioritize_queue():
    commander = CompanyCommander()
    tasks = commander.prioritize_queue()
    assert len(tasks) > 0
    # verify sorted descending
    scores = [t["score"] for t in tasks]
    assert scores == sorted(scores, reverse=True)