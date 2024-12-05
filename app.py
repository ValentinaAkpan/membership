import streamlit as st
import pandas as pd

# Streamlit UI for file upload
st.title("Non-Member Checker for Webinar Attendees")

st.write("Upload the Membership List and Webinar List CSV files to identify non-members by email.")

membership_file = st.file_uploader("Upload Membership List CSV", type=["csv"])
webinar_file = st.file_uploader("Upload Webinar List CSV", type=["csv"])

if membership_file and webinar_file:
    try:
        # Load the CSV files
        membership_data = pd.read_csv(membership_file, on_bad_lines='skip')  # Handle problematic rows
        webinar_data = pd.read_csv(webinar_file, on_bad_lines='skip')

        # Ensure both files have an 'Email' column
        if 'Email' not in membership_data.columns or 'Email' not in webinar_data.columns:
            st.error("Both files must have an 'Email' column.")
        else:
            # Extract email lists
            membership_list = membership_data['Email'].dropna().tolist()
            webinar_list = webinar_data['Email'].dropna().tolist()

            # Identify non-members
            non_members = [email for email in webinar_list if email not in membership_list]

            # Display non-members
            st.subheader("Non-Members")
            st.write(f"Total Non-Members: {len(non_members)}")
            
            if non_members:
                non_member_df = pd.DataFrame({"Email": non_members})
                st.write(non_member_df)

                # Allow downloading the non-members as CSV
                csv = non_member_df.to_csv(index=False)
                st.download_button(
                    label="Download Non-Members as CSV",
                    data=csv,
                    file_name="non_members.csv",
                    mime="text/csv"
                )
            else:
                st.write("No non-members found.")

    except Exception as e:
        st.error(f"Error processing files: {e}")
else:
    st.info("Please upload both files to proceed.")
