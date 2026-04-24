import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from html import escape
from pathlib import Path
from textwrap import dedent


st.set_page_config(
    page_title="Smart Shopping Web App",
    layout="wide",
    initial_sidebar_state="expanded",
)


DATASET_FILE = "amazon.csv"
STYLE_FILE = Path(__file__).with_name("style.css")
PLACEHOLDER_IMAGE = "https://placehold.co/640x420/F4E5D7/5D4037?text=No+Image"
REQUIRED_COLUMNS = [
    "product_id",
    "product_name",
    "category",
    "discounted_price",
    "actual_price",
    "discount_percentage",
    "rating",
    "rating_count",
    "img_link",
    "product_link",
]

def trim_text(text, limit=100):
    clean_text = " ".join(str(text).split())
    if len(clean_text) <= limit:
        return clean_text
    return clean_text[: limit - 3].rstrip() + "..."


def extract_numeric(series):
    cleaned = series.astype(str).str.replace(",", "", regex=False)
    numbers = cleaned.str.extract(r"(\d+(?:\.\d+)?)", expand=False)
    return pd.to_numeric(numbers, errors="coerce")


def clean_image_url(url):
    if not isinstance(url, str):
        return ""

    cleaned = url.strip()
    if not cleaned.startswith(("http://", "https://")):
        return ""

    cleaned = cleaned.replace("/images/W/WEBP_402378-T1/images/", "/images/")
    cleaned = cleaned.replace("/images/W/WEBP_402378-T2/images/", "/images/")
    cleaned = cleaned.replace("/images/W/WEBP_402378-T3/images/", "/images/")
    cleaned = cleaned.replace("/images/W/WEBP_402378-T4/images/", "/images/")
    return cleaned


@st.cache_data(show_spinner=False)
def load_data():
    df = pd.read_csv(DATASET_FILE).copy()
    df.columns = df.columns.str.strip().str.lower()

    missing_columns = [column for column in REQUIRED_COLUMNS if column not in df.columns]
    if missing_columns:
        raise ValueError("Missing required columns: " + ", ".join(missing_columns))

    df = df[REQUIRED_COLUMNS].copy()
    df = df.dropna(subset=["product_name", "category"])
    df["product_name"] = df["product_name"].astype(str).str.strip()
    df["category"] = (
        df["category"]
        .astype(str)
        .str.split("|")
        .str[0]
        .str.replace("&", " & ", regex=False)
        .str.replace(r"\s{2,}", " ", regex=True)
        .str.strip()
    )
    df["discounted_price"] = extract_numeric(df["discounted_price"])
    df["actual_price"] = extract_numeric(df["actual_price"])
    df["discount_percentage"] = extract_numeric(df["discount_percentage"])
    df["rating"] = extract_numeric(df["rating"])
    df["rating_count"] = extract_numeric(df["rating_count"]).fillna(0)
    df["img_link"] = df["img_link"].fillna("").astype(str).str.strip()
    df["image_url"] = df["img_link"].apply(clean_image_url)
    df["product_link"] = df["product_link"].fillna("").astype(str).str.strip()

    df = df.dropna(subset=["discounted_price", "rating"])
    df = df[df["discounted_price"] > 0]
    df = df[df["rating"].between(0, 5)]
    df = df.drop_duplicates(subset=["product_id"])
    df = df.sort_values(
        by=["category", "rating", "rating_count"],
        ascending=[True, False, False],
    ).reset_index(drop=True)

    return df


def format_price(value):
    if pd.isna(value):
        return "Price unavailable"
    return f"Rs. {float(value):,.0f}"


def make_product_pool(primary_df, backup_df, exclude_ids=None):
    exclude_ids = exclude_ids or []
    products = pd.concat([primary_df, backup_df], ignore_index=True)
    products = products[products["image_url"].astype(str).str.len() > 0]
    if exclude_ids:
        products = products[~products["product_id"].isin(exclude_ids)]
    return products.drop_duplicates(subset=["product_id"], keep="first").reset_index(drop=True)


def get_page_data(products, page_key, signature, page_size):
    signature_key = f"{page_key}_signature"
    if st.session_state.get(signature_key) != signature:
        st.session_state[page_key] = 0
        st.session_state[signature_key] = signature

    total_items = len(products)
    total_pages = max(1, (total_items + page_size - 1) // page_size)
    current_page = min(st.session_state.get(page_key, 0), total_pages - 1)
    st.session_state[page_key] = current_page

    start_index = current_page * page_size
    end_index = min(start_index + page_size, total_items)
    page_slice = products.iloc[start_index:end_index].copy()

    return page_slice, current_page, total_pages, start_index, end_index


def render_pagination_controls(page_key, total_items, current_page, total_pages, start_index, end_index):
    info_col, prev_col, next_col = st.columns([2.4, 1, 1])

    with info_col:
        if total_items == 0:
            st.caption("No products to display.")
        else:
            st.caption(
                f"Showing {start_index + 1}-{end_index} of {total_items} products"
            )

    with prev_col:
        if st.button(
            "Previous",
            key=f"{page_key}_prev",
            disabled=current_page == 0,
            use_container_width=True,
        ):
            st.session_state[page_key] = current_page - 1
            st.rerun()

    with next_col:
        if st.button(
            "Next",
            key=f"{page_key}_next",
            disabled=current_page >= total_pages - 1,
            use_container_width=True,
        ):
            st.session_state[page_key] = current_page + 1
            st.rerun()


def inject_styles():
    if not STYLE_FILE.exists():
        return

    css = STYLE_FILE.read_text(encoding="utf-8")
    st.markdown(f"<style>{css}</style>", unsafe_allow_html=True)


def render_hero(total_products, total_categories, dataset_name):
    st.markdown(
        dedent(
            f"""
            <div class="hero">
                <div class="hero-copy">
                    <span class="hero-tag">Data-driven shopping experience</span>
                    <h1>Smart Shopping Web App</h1>
                    <p>
                        Find better products faster with category filters, price limits, rating-based
                        recommendations, and a clean visual layout built fully in Streamlit.
                    </p>
                </div>
                <div class="hero-grid">
                    <div class="hero-stat">
                        <span class="hero-stat-label">Products loaded</span>
                        <span class="hero-stat-value">{int(total_products):,}</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-stat-label">Categories</span>
                        <span class="hero-stat-value">{int(total_categories):,}</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-stat-label">Dataset</span>
                        <span class="hero-stat-value">{escape(dataset_name)}</span>
                    </div>
                    <div class="hero-stat">
                        <span class="hero-stat-label">Recommendation type</span>
                        <span class="hero-stat-value">Rule-based</span>
                    </div>
                </div>
            </div>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def section_heading(label, title, description):
    st.markdown(
        dedent(
            f"""
            <div class="section-label">{escape(label)}</div>
            <h2 style="margin: 0 0 0.3rem 0; color: #2f241f;">{escape(title)}</h2>
            <p style="margin-top: 0; color: #70584d;">{escape(description)}</p>
            """
        ).strip(),
        unsafe_allow_html=True,
    )


def product_card_html(product, rank_label):
    name = escape(trim_text(product["product_name"], 110))
    category = escape(product["category"])
    image_url = escape(product["image_url"])
    product_url = (
        product["product_link"]
        if isinstance(product["product_link"], str)
        and product["product_link"].startswith(("http://", "https://"))
        else ""
    )
    rating_text = f"{float(product['rating']):.1f} / 5"
    rating_count_text = f"{int(product['rating_count']):,} ratings"

    actual_price_html = ""
    if pd.notna(product["actual_price"]) and product["actual_price"] > product["discounted_price"]:
        actual_price_html = f'<span class="actual-price">{format_price(product["actual_price"])}</span>'

    discount_html = ""
    if pd.notna(product["discount_percentage"]) and product["discount_percentage"] > 0:
        discount_html = f'<span class="discount-pill">{int(product["discount_percentage"])}% off</span>'

    if product_url:
        link_html = f'<a class="product-link" href="{escape(product_url)}" target="_blank" rel="noopener noreferrer">Open product</a>'
    else:
        link_html = ""

    price_extras = " ".join(part for part in [actual_price_html, discount_html] if part)
    link_section = link_html

    return dedent(
        f"""
        <div class="product-card">
            <div class="product-image-wrap">
                <img src="{image_url}" alt="product image">
                <span class="rating-badge">{rating_text}</span>
            </div>
            <div class="product-content">
                <p class="product-rank">{escape(rank_label)}</p>
                <div class="product-title">{name}</div>
                <p class="meta-line">{category}</p>
                <p class="meta-line">{rating_count_text}</p>
                <div class="price-row">
                    <span class="sale-price">{format_price(product["discounted_price"])}</span>{(" " + price_extras) if price_extras else ""}
                </div>
                {link_section if link_section else ""}
            </div>
        </div>
        """
    ).strip()


def render_product_grid(products, label_prefix):
    if products.empty:
        st.info("No products with valid images are available for this section.")
        return

    columns = st.columns(4)
    for index, (_, product) in enumerate(products.iterrows(), start=1):
        with columns[(index - 1) % 4]:
            st.markdown(
                product_card_html(product, f"{label_prefix} {index:02d}"),
                unsafe_allow_html=True,
            )


def pick_related_products(category_df, recommended_df):
    related_pool = category_df.loc[
        ~category_df["product_id"].isin(recommended_df["product_id"])
    ]
    if related_pool.empty:
        related_pool = category_df.copy()

    related_pool = related_pool.sort_values(
        by=["discounted_price", "rating"],
        ascending=[True, False],
    )
    return make_product_pool(
        related_pool,
        category_df.sort_values(by=["discounted_price", "rating"], ascending=[True, False]),
        exclude_ids=recommended_df["product_id"].tolist(),
    )


def render_price_distribution(df, selected_category, selected_price):
    sns.set_theme(style="whitegrid")
    all_prices = df["discounted_price"].dropna()
    category_prices = df.loc[df["category"] == selected_category, "discounted_price"].dropna()

    fig, ax = plt.subplots(figsize=(10, 4.6))
    fig.patch.set_facecolor("#fffaf4")
    ax.set_facecolor("#fffaf4")

    sns.histplot(
        all_prices,
        bins=22,
        color="#d8b28f",
        alpha=0.45,
        ax=ax,
        label="All products",
    )
    sns.histplot(
        category_prices,
        bins=22,
        color="#9f6d52",
        alpha=0.75,
        ax=ax,
        label=selected_category,
    )
    ax.axvline(
        selected_price,
        color="#365d4b",
        linestyle="--",
        linewidth=2.2,
        label=f"Selected max price: {format_price(selected_price)}",
    )
    ax.set_title("Price distribution across the dataset", fontsize=13, pad=12)
    ax.set_xlabel("Discounted price (Rs.)")
    ax.set_ylabel("Number of products")
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(frameon=False)

    st.pyplot(fig, use_container_width=True)
    plt.close(fig)


def build_sidebar(df, categories):
    st.sidebar.title("Filter Products")
    st.sidebar.caption("Choose a category and adjust the filters to refine recommendations.")

    selected_category = st.sidebar.selectbox("Category", categories)
    category_df = df[df["category"] == selected_category].copy()
    search_query = st.sidebar.text_input(
        "Search product name",
        placeholder="Type a keyword...",
    ).strip()
    max_price = int(category_df["discounted_price"].max())
    default_price = int(
        min(
            max_price,
            max(100, np.nanpercentile(category_df["discounted_price"], 75)),
        )
    )
    slider_step = max(50, max_price // 30) if max_price > 0 else 50

    selected_price = st.sidebar.slider(
        "Maximum price",
        min_value=0,
        max_value=max_price,
        value=default_price,
        step=slider_step,
    )
    selected_rating = st.sidebar.slider(
        "Minimum rating",
        min_value=0.0,
        max_value=5.0,
        value=4.0,
        step=0.1,
    )
    card_count = st.sidebar.slider(
        "Products per section",
        min_value=4,
        max_value=12,
        value=8,
        step=1,
    )

    st.sidebar.markdown("---")
    st.sidebar.write(f"Products in category: {len(category_df):,}")
    if search_query:
        search_count = category_df["product_name"].str.contains(
            search_query,
            case=False,
            na=False,
        ).sum()
        st.sidebar.write(f"Search matches: {search_count:,}")
    st.sidebar.write(f"Average rating: {category_df['rating'].mean():.2f}")
    st.sidebar.write(f"Median price: {format_price(category_df['discounted_price'].median())}")

    return selected_category, search_query, selected_price, selected_rating, card_count


def main():
    inject_styles()

    try:
        df = load_data()
    except Exception as exc:
        st.error(f"Unable to load the dataset: {exc}")
        st.stop()

    categories = sorted(df["category"].dropna().unique())
    if not categories:
        st.error("No valid categories were found after preprocessing.")
        st.stop()

    render_hero(len(df), len(categories), DATASET_FILE)

    selected_category, search_query, selected_price, selected_rating, card_count = build_sidebar(df, categories)

    category_df = df[df["category"] == selected_category].copy()
    search_df = category_df.copy()
    if search_query:
        search_df = search_df[
            search_df["product_name"].str.contains(search_query, case=False, na=False)
        ].copy()

    filtered_df = search_df[
        (search_df["discounted_price"] <= selected_price)
        & (search_df["rating"] >= selected_rating)
    ].copy()

    recommended_base = filtered_df.sort_values(
        by=["rating", "rating_count", "discounted_price"],
        ascending=[False, False, True],
    )

    recommended_pool = make_product_pool(
        recommended_base,
        recommended_base,
    )
    recommended_signature = (
        selected_category,
        search_query,
        selected_price,
        selected_rating,
        card_count,
        len(recommended_pool),
    )
    recommended_df, recommended_page, recommended_total_pages, recommended_start, recommended_end = get_page_data(
        recommended_pool,
        "recommended_page",
        recommended_signature,
        card_count,
    )

    related_pool = pick_related_products(search_df, recommended_df)
    related_signature = (
        selected_category,
        search_query,
        selected_price,
        selected_rating,
        card_count,
        recommended_page,
        tuple(recommended_df["product_id"].tolist()),
        len(related_pool),
    )
    related_df, related_page, related_total_pages, related_start, related_end = get_page_data(
        related_pool,
        "related_page",
        related_signature,
        card_count,
    )

    metric_1, metric_2, metric_3, metric_4 = st.columns(4)
    metric_1.metric("Selected category", selected_category)
    metric_2.metric("Matching products", f"{len(filtered_df):,}")
    metric_3.metric("Top rating", f"{category_df['rating'].max():.1f}")
    metric_4.metric("Lowest filtered price", format_price(filtered_df["discounted_price"].min()))

    if recommended_pool.empty:
        st.markdown(
            """
            <div class="note-box">
                No products match the current category, price, and rating filters. Try lowering the
                minimum rating, increasing the price range, or changing the search text.
            </div>
            """,
            unsafe_allow_html=True,
        )

    section_heading(
        "Recommendation block",
        "Recommended Products",
        "Products are filtered by category, search text, maximum price, and minimum rating, then ranked by quality.",
    )
    render_product_grid(recommended_df, "Pick")
    render_pagination_controls(
        "recommended_page",
        len(recommended_pool),
        recommended_page,
        recommended_total_pages,
        recommended_start,
        recommended_end,
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    section_heading(
        "Discovery block",
        "Customers Also Bought",
        "More items from the current category or search results, prioritizing affordable alternatives with solid ratings.",
    )
    render_product_grid(related_df, "More")
    render_pagination_controls(
        "related_page",
        len(related_pool),
        related_page,
        related_total_pages,
        related_start,
        related_end,
    )

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)

    chart_col, summary_col = st.columns([1.75, 1])
    with chart_col:
        section_heading(
            "Price insight",
            "Price Distribution",
            "Compare the selected category against the full dataset to understand product pricing trends.",
        )
        render_price_distribution(df, selected_category, selected_price)

    with summary_col:
        section_heading(
            "Project snapshot",
            "How this app works",
            "This is a rule-based shopping recommender built with simple filtering logic.",
        )
        st.markdown(
            """
            <div class="note-box">
                <strong>Core flow:</strong><br/>
                1. Clean the raw Amazon dataset.<br/>
                2. Filter products by category, price, and rating.<br/>
                3. Rank matches by rating and rating count.<br/>
                4. Show affordable alternatives from the same category.
            </div>
            <div class="note-box">
                <strong>Tools used:</strong><br/>
                Streamlit for the UI, Pandas and NumPy for processing, and Matplotlib plus
                Seaborn for price visualization.
            </div>
            """,
            unsafe_allow_html=True,
        )


if __name__ == "__main__":
    main()
