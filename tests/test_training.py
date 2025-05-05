from unittest.mock import patch, MagicMock
from src.training.train_model import train_and_save_model

@patch("src.training.train_model.mlflow.set_experiment")
@patch("src.training.train_model.mlflow.start_run")
@patch("src.training.train_model.mlflow.log_params")
@patch("src.training.train_model.mlflow.log_metric")
@patch("src.training.train_model.mlflow.sklearn.log_model")
def test_train_model(mock_log_model, mock_log_metric, mock_log_params, mock_start_run, mock_set_experiment):
    mock_start_run.return_value.__enter__.return_value = MagicMock()
    accuracy = train_and_save_model()
    assert 0.5 <= accuracy <= 1.0
