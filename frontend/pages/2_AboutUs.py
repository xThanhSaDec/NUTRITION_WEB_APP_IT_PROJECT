"""
About Us Page - Team Information and Project Details
Learn about the development team and project background
"""
import streamlit as st
import requests
import json
import base64
from pathlib import Path


# Configure page
st.set_page_config(
    page_title="About Us",
    page_icon="👥",
    layout="wide"
)

# Backend API configuration
BACKEND_URL = "http://127.0.0.1:8000"

def load_logo_base64(logo_filename="logo.png"):
    """Load logo from assets/icons and convert to base64"""
    try:
        logo_path = Path(__file__).parent.parent / "assets" / "icons" / logo_filename
        if logo_path.exists():
            with open(logo_path, "rb") as img_file:
                return base64.b64encode(img_file.read()).decode()
        else:
            print(f"Logo not found: {logo_path}")
            return None
    except Exception as e:
        print(f"Error loading logo: {e}")
        return None
    
def apply_about_css():
    """Apply custom CSS for about page"""
    st.markdown("""
    <style>
        .about-header {
            background: linear-gradient(135deg, #9b59b6 0%, #8e44ad 100%);
            padding: 2.5rem;
            border-radius: 15px;
            text-align: center;
            color: white;
            margin-bottom: 2rem;
            box-shadow: 0 10px 30px rgba(155, 89, 182, 0.3);
        }
        
        .about-header h1 {
            font-size: 2.5rem;
            margin-bottom: 0.5rem;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.3);
        }
        
        .team-card {
            background: linear-gradient(135deg, #f8f9fa 0%, #e9ecef 100%);
            padding: 2rem;
            border-radius: 15px;
            margin: 1.5rem 0;
            box-shadow: 0 8px 25px rgba(0,0,0,0.1);
            border-left: 5px solid #3498db;
            transition: transform 0.3s ease;
        }
        
        .team-card:hover {
            transform: translateY(-5px);
        }
        
        .team-member-name {
            color: #2c3e50;
            font-size: 1.3rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .team-member-role {
            color: #3498db;
            font-size: 1rem;
            font-weight: 600;
            margin-bottom: 1rem;
        }
        
        .team-member-id {
            background: #3498db;
            color: white;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            font-weight: bold;
            display: inline-block;
            margin-bottom: 1rem;
        }
        
        .skill-tag {
            background: #e8f4fd;
            color: #2980b9;
            padding: 0.3rem 0.8rem;
            border-radius: 15px;
            font-size: 0.8rem;
            margin: 0.2rem;
            display: inline-block;
            border: 1px solid #bdd8f1;
        }
        
        .project-stats {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
            gap: 1.5rem;
            margin: 2rem 0;
        }
        
        .stat-card {
            background: linear-gradient(135deg, #3498db, #2980b9);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            box-shadow: 0 6px 20px rgba(52, 152, 219, 0.3);
        }
        
        .stat-number {
            font-size: 2.2rem;
            font-weight: bold;
            margin-bottom: 0.5rem;
        }
        
        .stat-label {
            font-size: 0.9rem;
            opacity: 0.9;
        }
        
        .tech-section {
            background: #EDC213;
            padding: 2rem;
            border-radius: 12px;
            border-left: 4px solid #f39c12;
            margin: 2rem 0;
        }
        
        .tech-grid {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 1.5rem;
            margin-top: 1.5rem;
        }
        
        .tech-item {
            background: #1B4FD1;
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 4px 15px rgba(0,0,0,0.1);
            text-align: center;
        }
        
        .tech-icon {
            font-size: 2rem;
            margin-bottom: 1rem;
        }
        
        .contribution-list {
            background: #f8f9fa;
            padding: 1rem;
            border-radius: 8px;
            margin-top: 1rem;
        }
        
        .contribution-list ul {
            margin: 0;
            padding-left: 1.2rem;
        }
        
        .contribution-list li {
            margin: 0.5rem 0;
            color: #5a6c7d;
        }
        
        .supervisor-info {
            background: linear-gradient(135deg, #2ecc71, #27ae60);
            color: white;
            padding: 1.5rem;
            border-radius: 12px;
            text-align: center;
            margin: 2rem 0;
            box-shadow: 0 6px 20px rgba(46, 204, 113, 0.3);
        }
        
        .project-timeline {
            background: #43DE98;
            padding: 1.5rem;
            border-radius: 12px;
            border-left: 4px solid #1abc9c;
            margin: 1.5rem 0;
        }
        .top-logo {
                    position: absolute;
                    top: -230px;
                    left: -15px;
                    z-index: 999999;
                    display: flex;
                    align-items: center;
                    gap: 8px;
                    /* Màu adaptive với system theme */
                    background: var(--background-color, #fafafa);
                    border: 0px solid var(--border-color, #e0e0e0);
                    color: var(--text-color, #262730);
                    padding: 4px 12px;
                    border-radius: 8px;
                    transition: all 0.3s ease;
                }
                
                /* Dark theme override */
                @media (prefers-color-scheme: dark) {
                    .top-logo {
                        background: #262730;
                        border-color: #3a3b47;
                        color: #fafafa;
                    }
                }
                
                .top-logo img {
                    width: 37px;
                    height: 37px;
                    border-radius: 4px;
                    object-fit: cover;
                }
                
                .top-logo span {
                    font-weight: 600;
                    color: #333;
                    font-size: 14px;
                }
                
    </style>
    """, unsafe_allow_html=True)


    
def get_team_info_from_api():
    """Fetch team information from backend API"""
    try:
        response = requests.get(f"{BACKEND_URL}/api/aboutus/team", timeout=5)
        if response.status_code == 200:
            return response.json()
        else:
            return None
    except:
        return None


def render_team_member(member_data):
    """Render individual team member card"""
    name = member_data.get('name', 'Unknown')
    student_id = member_data.get('student_id', 'N/A')
    role = member_data.get('primary_role', 'Team Member')
    skills = member_data.get('skills', [])
    contributions = member_data.get('contributions', [])
    
    st.markdown(f"""
    <div class="team-card">
        <div class="team-member-name">{name}</div>
        <div class="team-member-id">Student ID: {student_id}</div>
        <div class="team-member-role">{role}</div>
    </div>
    """, unsafe_allow_html=True)
    
    # if skills:
    #     st.markdown("** Technical Skills:**")
    #     skills_html = "".join([f'<span class="skill-tag">{skill}</span>' for skill in skills])
    #     st.markdown(skills_html, unsafe_allow_html=True)
    
    # if contributions:
    #     st.markdown("** Key Contributions:**")
    #     st.markdown(f"""
    #     <div class="contribution-list">
    #         <ul>
    #             {"".join([f"<li>{contrib}</li>" for contrib in contributions])}
    #         </ul>
    #     </div>
    #     """, unsafe_allow_html=True)

def main():
    """Main about page function"""
    apply_about_css()
    
    # Header
    st.markdown("""
    <div class="about-header">
        <h1> About Our Team</h1>
        <p>Meet the developers behind the Food Recognition & Nutrition Web Application</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project supervisor
    st.markdown("""
    <div class="supervisor-info">
        <h3> Project Supervisor</h3>
        <h2>Assoc. Prof. Dr. Hoang Van Dung</h2>
        <p>Academic supervisor for this 15-week IT project focusing on computer vision and web application development</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Try to get team info from API
    team_data = get_team_info_from_api()
    
    if team_data and team_data.get('members'):
        st.markdown("## Development Team")

        # Display team statistics
        st.markdown(f"""
        <div class="project-stats">
            <div class="stat-card">
                <div class="stat-number">{team_data.get('team_size', 3)}</div>
                <div class="stat-label">Team Members</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">15</div>
                <div class="stat-label">Project Weeks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">Tech Domains</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">2025</div>
                <div class="stat-label">Academic Year</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Display team members
        for member in team_data['members']:
            render_team_member(member)
        
        # Collaboration tools
        if team_data.get('collaboration_tools'):
            st.markdown("## Development Tools & Collaboration")
            tools = team_data['collaboration_tools']
            tools_text = " • ".join(tools)
            st.info(f"*Tools Used:* {tools_text}")
    
    else:
        # Fallback team information if API is not available
        st.markdown("## Development Team")

        # Team statistics
        st.markdown("""
        <div class="project-stats">
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">Team Members</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">15</div>
                <div class="stat-label">Project Weeks</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">3</div>
                <div class="stat-label">Tech Domains</div>
            </div>
            <div class="stat-card">
                <div class="stat-number">2025</div>
                <div class="stat-label">Academic Year</div>
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        # Team members (fallback data)
        team_members = [
            {
                "name": "Tran Dinh Khuong",
                "student_id": "23110035",
                "primary_role": "Lead Developer & ML Engineer",
            },
            {
                "name": "Nguyen Nhat Phat",
                "student_id": "23110053",
                "primary_role": "Backend Developer & API Engineer", 
                # "skills": ["FastAPI", "RESTful APIs", "Database Management", "Async Programming", "API Documentation"],
                # "contributions": [
                #     "FastAPI application architecture design",
                #     "RESTful endpoints implementation",
                #     "Database design and optimization",
                #     "API documentation and testing"
                # ]
            },
            {
                "name": "Tran Huynh Xuan Thanh",
                "student_id": "23110060",
                "primary_role": "Frontend Developer & UI/UX Designer",
                # "skills": ["Streamlit", "UI/UX Design", "Web Technologies", "User Experience", "Responsive Design"],
                # "contributions": [
                #     "Streamlit application development",
                #     "User interface design and optimization",
                #     "User experience research and implementation", 
                #     "Frontend-backend integration"
                # ]
            }
        ]
        
        for member in team_members:
            render_team_member(member)
    
    # Technical architecture section
    st.markdown("## Technical Architecture")
    
    st.markdown("""
    <div class="tech-section">
        <h3> Our Technology Stack</h3>
        <p>We've carefully selected modern technologies to build a robust, scalable, and user-friendly application.</p>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="tech-grid">
        <div class="tech-item">
            <div class="tech-icon"></div>
            <h4>Machine Learning</h4>
            <p><strong>ResNet50 CNN</strong><br>
            TensorFlow & Keras<br>
            Transfer Learning<br>
            131 Food Categories</p>
        </div>
        <div class="tech-item">
            <div class="tech-icon"></div>
            <h4>Backend API</h4>
            <p><strong>FastAPI Framework</strong><br>
            RESTful Architecture<br>
            Async Processing<br>
            OpenAPI Documentation</p>
        </div>
        <div class="tech-item">
            <div class="tech-icon"></div>
            <h4>Frontend Interface</h4>
            <p><strong>Streamlit Framework</strong><br>
            Responsive Design<br>
            Interactive Widgets<br>
            Real-time Updates</p>
        </div>

    </div>
    """, unsafe_allow_html=True)
            # <div class="tech-item">
        #     <div class="tech-icon"></div>
        #     <h4>Data Management</h4>
        #     <p><strong>CSV Database</strong><br>
        #     JSON Class Mapping<br>
        #     Pandas Processing<br>
        #     Efficient Retrieval</p>
        # </div>
    # Project timeline
    st.markdown("## Project Timeline")
    
    st.markdown("""
    <div class="project-timeline">
        <h4>15-Week Development Timeline</h4>
        <p><strong>Weeks 1-3:</strong> Research, planning, and technology selection</p>
        <p><strong>Weeks 4-6:</strong> Data collection and model training</p>
        <p><strong>Weeks 7-9:</strong> Backend API development</p>
        <p><strong>Weeks 10-12:</strong> Frontend application development</p>
        <p><strong>Weeks 13-15:</strong> Integration, testing, and documentation</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Project goals and impact
    # st.markdown("#Project Goals & Impact")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Primary Objectives
        - **AI-Powered Recognition:** Achieve high accuracy in food identification
        - **Nutritional Insights:** Provide comprehensive dietary information
        - **User Experience:** Create an intuitive and responsive interface
        - **Cultural Inclusion:** Support both international and Vietnamese cuisine
        - **Real-time Performance:** Ensure fast processing for practical use
        """)
    
    with col2:
        st.markdown("""
        #### Potential Applications
        - **Personal Health:** Daily nutrition tracking and management
        - **Healthcare:** Support for dietitians and nutritionists
        - **Education:** Interactive learning about nutrition
        - **Restaurant Industry:** Accurate nutritional information display
        - **Research:** Food consumption pattern analysis
        """)
    
    # Future enhancements
    st.markdown("#### Future Enhancements")
    
    future_features = [
        "Object detection for multiple food items in one image",
        "Mobile application development for iOS and Android",
        "Expanded food database with regional cuisines",
        "User feedback system for continuous model improvement",
        "Personal nutrition tracking and analytics dashboard",
        "Integration with popular health and fitness apps"
    ]
    
    for feature in future_features:
        st.markdown(f"- {feature}")
    
    # Contact and links section
    st.markdown("#Contact & Resources")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        ### Project Links
        - *GitHub Repository:** [View Source Code](https://github.com/xThanhSaDec/NUTRITION_WEB_APP_IT_PROJECT)
        - *API Documentation:** [FastAPI Docs](http://127.0.0.1:8000/docs)
        - *Project Report:** Available upon request
        """)
    
    with col2:
        st.markdown("""
        ### Academic Information
        - **Institution:** HCMC University of Technology and Education
        - **Course:** IT Project (15 weeks)
        - **Year:** 2025
        - **Supervisor:** Assoc. Prof. Dr. Hoang Van Dung
        """)
    
    # Sidebar navigation
    with st.sidebar:
        # st.markdown("#Quick Navigation")
        # Logo header
        logo_base64 = load_logo_base64("LOGO HCMUTE.png")
        if logo_base64:
            st.markdown(f"""
            <div class="top-logo">
                <img src="data:image/png;base64,{logo_base64}" alt="Logo">
                <h3>Food Recognition & Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
        else:
            st.markdown("""
            <div class="top-logo">
                <span style="font-size: 20px;">🍽️</span>
                <h3>Food Recognition & Analysis</h3>
            </div>
            """, unsafe_allow_html=True)
            
        if st.button(" Home Page", use_container_width=True):
            st.switch_page("streamlit_app.py")
        
        if st.button(" Prediction Page", use_container_width=True):
            st.switch_page("pages/1_Predict.py")
        
        st.markdown("---")
        # st.markdown("#Team Stats")
        st.info("""
        **Project Overview:**
        - 3 dedicated developers
        - 15 weeks of development
        - 131 food categories supported
        - 3 Roles: ML, Dataset, Frontend&Backend
        """)

        # st.markdown("#Academic Context")
        st.info("""
        This project represents the culmination of our IT studies, combining:
        - Advanced machine learning techniques
        - Modern web development practices
        - User-centered design principles
        - Industry-standard development tools
        """)

if __name__ == "__main__":
    main()