import streamlit as st
import instaloader
import pandas as pd
from concurrent.futures import ThreadPoolExecutor

def get_modified_reel_link(insta_url):
    L = instaloader.Instaloader()  # Create a new Instaloader instance for each call
    try:
        # Extract shortcode from URL
        parts = insta_url.rstrip("/").split("/")
        shortcode = parts[-1] if parts[-2] in ["reel", "p"] else parts[-2]
        
        # Get the post object from shortcode
        post = instaloader.Post.from_shortcode(L.context, shortcode)
        username = post.owner_username

        # Always return in "reel" format
        return f"https://www.instagram.com/{username}/reel/{shortcode}/"
    
    except Exception as e:
        return f"Error: {e}"

st.title("Instagram Reel Link Modifier")

st.markdown("""
Enter your Instagram Post/Reel URLs (one per line). The app will extract the username and convert all links to the reel format.
""")

# Text area for input
insta_urls_input = st.text_area("Enter Instagram Post/Reel URLs:")

if st.button("Process"):
    # Split input into a list of non-empty URLs
    insta_urls = [url.strip() for url in insta_urls_input.splitlines() if url.strip()]

    if not insta_urls:
        st.error("Please enter at least one valid Instagram URL.")
    else:
        st.info("Processing URLs. Please wait...")

        # Process URLs concurrently
        with ThreadPoolExecutor(max_workers=10) as executor:
            modified_urls = list(executor.map(get_modified_reel_link, insta_urls))

        # Create a DataFrame with original and modified URLs
        df = pd.DataFrame({
            "Original URL": insta_urls,
            "Modified Reel URL": modified_urls
        })

        st.success("Processing complete!")
        st.dataframe(df)

        # Convert DataFrame to CSV
        csv = df.to_csv(index=False).encode("utf-8")

        # Download button for CSV
        st.download_button(
            label="Download CSV",
            data=csv,
            file_name="modified_reel_urls.csv",
            mime="text/csv"
        )
