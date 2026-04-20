from src.core import SwarmEngine, aggregate_votes, analyze_disagreement, calibrate_confidence


def test_init(): assert SwarmEngine().get_stats()["ops"] == 0
def test_op(): c = SwarmEngine(); c.optimize(x=1); assert c.get_stats()["ops"] == 1
def test_multi(): c = SwarmEngine(); [c.optimize() for _ in range(5)]; assert c.get_stats()["ops"] == 5
def test_reset(): c = SwarmEngine(); c.optimize(); c.reset(); assert c.get_stats()["ops"] == 0


def test_vote_aggregation_reports_winner_and_confidence():
    summary = aggregate_votes([
        {"label": "approve"},
        {"label": "approve"},
        {"label": "reject"},
    ])
    assert summary["winner"] == "approve"
    assert summary["confidence"] == 0.667


def test_disagreement_analysis_and_calibration():
    report = analyze_disagreement([
        {"label": "approve"},
        {"label": "reject"},
        {"label": "approve"},
        {"label": "abstain"},
    ])
    assert report["disagreement"] > 0
    assert "abstain" in report["minority_labels"]
    assert calibrate_confidence(report["raw_confidence"], report["disagreement"]) < report["raw_confidence"]


def test_engine_exposes_calibrated_swarm_summary():
    engine = SwarmEngine()
    summary = engine.aggregate_prediction([
        {"label": "ship"},
        {"label": "ship"},
        {"label": "hold"},
    ])
    assert summary["winner"] == "ship"
    assert summary["calibrated_confidence"] <= summary["confidence"]
