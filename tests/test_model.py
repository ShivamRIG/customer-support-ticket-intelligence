import pytest
from src.model.predict import TicketTriagePipeline, get_triage_pipeline

@pytest.fixture(scope="module")
def pipeline():
    return get_triage_pipeline()

def test_pipeline_loading(pipeline):
    assert pipeline is not None
    assert pipeline.clf_queue is not None
    assert pipeline.clf_priority is not None

def test_pipeline_prediction_output(pipeline):
    result = pipeline.predict(
        subject="Database connection timeout",
        body="Primary Postgres pool exhausted returning 504 errors.",
        answer="Checking replication lag."
    )
    
    assert "suggested_queue" in result
    assert "suggested_priority" in result
    assert isinstance(result["suggested_queue"], str)
    assert isinstance(result["suggested_priority"], str)
    assert len(result["suggested_queue"]) > 0
    assert len(result["suggested_priority"]) > 0

def test_pipeline_empty_answer(pipeline):
    # Ensure optional 'answer' parameter defaults safely when empty
    result = pipeline.predict(
        subject="Password reset failure",
        body="User cannot receive OTP emails."
    )
    assert result["suggested_queue"] is not None
    assert result["suggested_priority"] is not None