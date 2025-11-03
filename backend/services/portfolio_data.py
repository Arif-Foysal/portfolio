"""
Portfolio data service containing information about skills, projects, education, etc.
This would typically come from a database, but for this example, we'll use static data.
"""

from typing import List, Dict, Any
from models import ProjectData, SkillData, EducationData, ExperienceData, AchievementData, ContactData

class PortfolioDataService:
    """Service class to manage portfolio data"""
    
    def __init__(self):
        self._load_portfolio_data()
    
    def _load_portfolio_data(self):
        """Load portfolio data - replace with database queries in production"""
        
        # Projects data
        self.projects = [
            ProjectData(
                name="Skin Disease Detection System",
                description="AI-powered mobile application for detecting skin diseases using computer vision and deep learning",
                technologies=["Python", "TensorFlow", "Flutter", "FastAPI", "OpenCV"],
                link="https://example.com/skin-detection",
                github_link="https://github.com/arif-foysal/skin-detection",
                image="/projects/skin-detection.jpg"
            ),
            ProjectData(
                name="Portfolio Website",
                description="Modern responsive portfolio website built with Nuxt 3, featuring dynamic content and interactive animations",
                technologies=["Nuxt.js", "Vue.js", "TypeScript", "Tailwind CSS", "FastAPI"],
                link="https://arif.it.com",
                github_link="https://github.com/arif-foysal/portfolio",
                image="/projects/portfolio.jpg"
            ),
            ProjectData(
                name="E-commerce Analytics Dashboard",
                description="Real-time analytics dashboard for e-commerce businesses with advanced reporting and insights",
                technologies=["React", "Node.js", "MongoDB", "Chart.js", "Express"],
                link="https://example.com/analytics",
                github_link="https://github.com/arif-foysal/analytics",
                image="/projects/analytics.jpg"
            )
        ]
        
        # Skills data
        self.skills = [
            SkillData(
                category="Frontend Development",
                skills=["React", "Vue.js", "Nuxt.js", "TypeScript", "Tailwind CSS", "HTML5", "CSS3"],
                proficiency="Advanced"
            ),
            SkillData(
                category="Backend Development",
                skills=["Python", "FastAPI", "Node.js", "Express", "PostgreSQL", "MongoDB"],
                proficiency="Advanced"
            ),
            SkillData(
                category="Mobile Development",
                skills=["Flutter", "React Native", "Dart", "Android Studio"],
                proficiency="Intermediate"
            ),
            SkillData(
                category="AI/ML",
                skills=["TensorFlow", "PyTorch", "Scikit-learn", "OpenCV", "LangChain"],
                proficiency="Intermediate"
            ),
            SkillData(
                category="DevOps & Cloud",
                skills=["Docker", "AWS", "Vercel", "Git", "GitHub Actions", "Linux"],
                proficiency="Intermediate"
            )
        ]
        
        # Education data
        self.education = [
            EducationData(
                institution="University of Technology",
                degree="Bachelor of Science",
                field="Computer Science and Engineering",
                year="2020-2024",
                description="Specialized in software engineering and artificial intelligence"
            ),
            EducationData(
                institution="Tech Academy",
                degree="Certificate",
                field="Full Stack Web Development",
                year="2022",
                description="Intensive bootcamp covering modern web development technologies"
            )
        ]
        
        # Experience data
        self.experience = [
            ExperienceData(
                company="Tech Solutions Inc.",
                position="Full Stack Developer",
                duration="2023 - Present",
                description="Developing scalable web applications and AI-powered solutions for enterprise clients",
                technologies=["React", "Python", "FastAPI", "PostgreSQL", "AWS"]
            ),
            ExperienceData(
                company="StartupXYZ",
                position="Frontend Developer Intern",
                duration="2022 - 2023",
                description="Built responsive user interfaces and collaborated on mobile app development",
                technologies=["Vue.js", "Nuxt.js", "Flutter", "Firebase"]
            )
        ]
        
        # Achievements data
        self.achievements = [
            AchievementData(
                title="Best Innovation Award",
                description="Won first place in university hackathon for AI-powered skin disease detection app",
                date="2023",
                link="https://example.com/award"
            ),
            AchievementData(
                title="Open Source Contributor",
                description="Active contributor to popular open-source projects with 50+ merged PRs",
                date="2022-Present"
            ),
            AchievementData(
                title="Tech Conference Speaker",
                description="Presented on 'AI in Healthcare Applications' at regional tech conference",
                date="2023"
            )
        ]
        
        # Contact data
        self.contact = ContactData(
            email="arif@example.com",
            linkedin="https://linkedin.com/in/arif-foysal",
            github="https://github.com/arif-foysal",
            website="https://arif.it.com"
        )
    
    def get_projects(self) -> List[ProjectData]:
        """Get all projects"""
        return self.projects
    
    def get_project_by_name(self, name: str) -> ProjectData | None:
        """Get a specific project by name"""
        for project in self.projects:
            if name.lower() in project.name.lower():
                return project
        return None
    
    def get_skills(self) -> List[SkillData]:
        """Get all skills"""
        return self.skills
    
    def get_education(self) -> List[EducationData]:
        """Get education information"""
        return self.education
    
    def get_experience(self) -> List[ExperienceData]:
        """Get work experience"""
        return self.experience
    
    def get_achievements(self) -> List[AchievementData]:
        """Get achievements"""
        return self.achievements
    
    def get_contact_info(self) -> ContactData:
        """Get contact information"""
        return self.contact
    
    def search_projects(self, query: str) -> List[ProjectData]:
        """Search projects by query"""
        query_lower = query.lower()
        return [
            project for project in self.projects
            if query_lower in project.name.lower() or 
               query_lower in project.description.lower() or
               any(tech.lower() in query_lower for tech in project.technologies)
        ]
    
    def get_personal_info(self) -> Dict[str, Any]:
        """Get general personal information"""
        return {
            "name": "Arif Foysal",
            "title": "Full Stack Developer & AI Enthusiast",
            "location": "Bangladesh",
            "bio": "Passionate software developer with expertise in full-stack web development and artificial intelligence. I love building innovative solutions that solve real-world problems.",
            "years_of_experience": 3,
            "specialization": ["Web Development", "AI/ML", "Mobile Apps"]
        }

# Create global instance
portfolio_service = PortfolioDataService()
