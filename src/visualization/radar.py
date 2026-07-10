import os
import numpy as np
import matplotlib.pyplot as plt


def create_radar(
    company_name,
    company_values,
    peer_values,
    labels,
    output_file
):
    # Number of metrics
    num_vars = len(labels)

    # Create angles
    angles = np.linspace(
        0,
        2 * np.pi,
        num_vars,
        endpoint=False
    ).tolist()

    # Close the polygon
    angles += angles[:1]
    company_values = company_values + company_values[:1]
    peer_values = peer_values + peer_values[:1]

    # Create figure
    fig, ax = plt.subplots(
        figsize=(6, 6),
        subplot_kw=dict(polar=True)
    )

    # Company polygon
    ax.plot(
        angles,
        company_values,
        linewidth=2,
        label=company_name
    )

    ax.fill(
        angles,
        company_values,
        alpha=0.25
    )

    # Peer average polygon
    ax.plot(
        angles,
        peer_values,
        linestyle="--",
        linewidth=2,
        label="Peer Average"
    )

    # Axis labels
    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(labels)

    # Title
    ax.set_title(company_name)

    # Legend
    ax.legend(loc="upper right")

    # Create folder if needed
    os.makedirs(
        os.path.dirname(output_file),
        exist_ok=True
    )

    # Save image
    plt.savefig(
        output_file,
        dpi=300,
        bbox_inches="tight"
    )

    plt.close()