import pandas as pd
import numpy as np
import click
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.metrics import accuracy_score, classification_report
from icecream import ic
import matplotlib.pyplot as plt


@click.command()
@click.option(
    "--path",
    default="data/CIC/flows_labeled/Thursday-WorkingHours-Afternoon-Infilteration.pcap_ISCX.csv",
)
@click.option(
    "--model_type", type=click.Choice(["random_forest", "knn"]), default="knn"
)
def main(path: str, model_type: str) -> None:
    df = load_data(path)
    df, x_pca, y, scaler = process_data(df)
    ic(df["Label"].unique())

    model = train(x_pca, y, model_type)
    df = analyze_predictions(df, model, x_pca)
    get_metrics(df)
    plot_clusters(x_pca, df["PredictedLabel"], model_type)


def load_data(path: str) -> pd.DataFrame:
    df = pd.read_csv(path)
    df.columns = df.columns.str.strip().str.replace(" ", "_")
    return df


def process_data(df: pd.DataFrame, scaler: StandardScaler | None = None):
    df = df.drop(
        ["Flow_ID", "Source_IP", "Destination_IP", "Timestamp"], axis=1, errors="ignore"
    )

    x = df.select_dtypes(include=[np.number])
    x.replace([np.inf, -np.inf], np.nan, inplace=True)
    x.fillna(x.mean(), inplace=True)

    scaler = StandardScaler() if scaler is None else scaler
    x_scaled = scaler.fit_transform(x)

    pca = PCA(n_components=0.95)
    x_pca = pca.fit_transform(x_scaled)

    y = df["Label"].astype("category").cat.codes

    return df, x_pca, y, scaler


def train(x_pca, y, model_type: str) -> RandomForestClassifier | KNeighborsClassifier:
    models = {
        "random_forest": RandomForestClassifier(
            n_estimators=50,
            max_depth=10,
            random_state=42,
        ),
        "knn": KNeighborsClassifier(
            n_neighbors=5,  # You can adjust the number of neighbors
        ),
    }
    model = models.get(model_type)
    model.fit(x_pca, y)
    return model


def get_metrics(df: pd.DataFrame):
    accuracy = accuracy_score(df["Label"], df["PredictedLabel"])
    report = classification_report(df["Label"], df["PredictedLabel"])
    print(f"Accuracy: {accuracy * 100:.2f}%")
    print(report)


def analyze_predictions(df: pd.DataFrame, model, x_pca):
    predictions = model.predict(x_pca)
    label_mapping = {
        i: label
        for i, label in enumerate(df["Label"].astype("category").cat.categories)
    }
    df["PredictedLabel"] = pd.Series(predictions).map(label_mapping)
    return df


def plot_clusters(x_pca, predictions, model_name):
    pca = PCA(n_components=2)
    x_pca_reduced = pca.fit_transform(x_pca)

    unique_labels = predictions.unique()
    label_mapping = {label: idx for idx, label in enumerate(unique_labels)}
    numeric_predictions = predictions.map(label_mapping)

    plt.figure(figsize=(10, 7))
    scatter = plt.scatter(
        x_pca_reduced[:, 0],
        x_pca_reduced[:, 1],
        c=numeric_predictions,
        cmap="viridis",
        s=10,
        alpha=0.7,
    )

    handles, _ = scatter.legend_elements()
    legend_labels = [label for label in unique_labels]
    plt.legend(handles, legend_labels, title="Predicted Labels")
    plt.xlabel("PCA 1")
    plt.ylabel("PCA 2")

    plt.xlim(0, 30)
    plt.ylim(-10, 30)

    plt.show()
    plt.savefig(f"data/clustering/plots/{model_name}.png")


if __name__ == "__main__":
    main()
