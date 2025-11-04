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
                name="Blue Horizon ROV",
                description="An advanced Remotely Operated Vehicle (ROV) designed for underwater exploration and research. Equipped with high-definition cameras, sonar systems, and robotic arms, it enables scientists to study marine environments in detail while ensuring safety and efficiency.",
                technologies=["Raspberry Pi", "ESP32", "Arduino", "C++", "Python", "Flask", "JavaScript", "WebRTC"],
                link="https://example.com/blue-horizon",
                github_link="https://github.com/arif-foysal/blue-horizon-rov",
                image="/projects/blue-horizon/main.jpg"
            ),
            ProjectData(
                name="Adventure Amigos",
                description="A smart tourism web application designed to make traveling seamless and enjoyable. Adventure Amigos allows users to plan trips, book tours and accommodations, discover local businesses, and explore historical sites — all in one unified platform powered by AI-driven personalization and multilingual support.",
                technologies=["PHP", "MySQL", "JavaScript", "Vue.js", "TailwindCSS", "AI Integration"],
                link="https://example.com/adventure-amigos",
                github_link="https://github.com/arif-foysal/adventure-amigos",
                image="/projects/adventure-amigos.jpg"
            ),
            ProjectData(
                name="SkinCheck AI",
                description="SkinCheck AI is an intelligent skin disease detection platform that uses deep learning to classify skin lesions as benign or malignant. Trained on the HAM10000 dataset, it combines a FastAPI backend, Supabase authentication, and secure cloud deployment to deliver accurate real-time predictions from uploaded skin images.",
                technologies=["FastAPI", "Python", "Supabase", "TensorFlow", "Deep Learning", "JWT Auth"],
                link="https://example.com/skincheck-ai",
                github_link="https://github.com/arif-foysal/skincheck-ai",
                image="/projects/skincheck-ai.jpg"
            ),
            ProjectData(
                name="Resumind",
                description="Resumind is an AI-powered resume builder that helps users create professional, personalized, and ATS-friendly resumes in minutes. Built with Nuxt for an elegant, interactive interface and Django for scalable backend APIs, it integrates OpenAI's generative models to automatically craft job descriptions, summarize achievements, and tailor content for specific roles.",
                technologies=["Nuxt", "Django", "TailwindCSS", "LangGraph", "OpenAI API", "ChromaDB", "PostgreSQL", "JWT Auth"],
                link="https://arif.it.com/projects/resumind",
                github_link="https://github.com/arif-foysal/resumind",
                image="/projects/resumind.jpg"
            ),
            ProjectData(
                name="ESP32 Vehicle Tracker",
                description="ESP32 Vehicle Tracker is a real-time vehicle monitoring and control system powered by MicroPython and FastAPI. It enables live tracking, collision detection, and remote vehicle control via a cloud dashboard. The system integrates sensor data, secure cloud APIs, and a modern web interface for reliable and accessible fleet management.",
                technologies=["FastAPI", "MicroPython", "ESP32", "WebSocket", "Real-Time"],
                link="https://esp32-vehicle-tracker.onrender.com",
                github_link="https://github.com/Arif-Foysal/esp32-vehicle-tracker",
                image="/projects/esp32-tracker.jpg"
            ),
            ProjectData(
                name="Portfolio Website",
                description="Modern responsive portfolio website built with Nuxt 3, featuring dynamic content, interactive animations, and AI-powered chat functionality",
                technologies=["Nuxt.js", "Vue.js", "TypeScript", "Tailwind CSS", "FastAPI"],
                link="https://arif.it.com",
                github_link="https://github.com/arif-foysal/portfolio",
                image="/projects/portfolio.jpg"
            )
        ]
        
        # Skills data
        self.skills = [
            SkillData(
                category="Frontend Development",
                skills=["Vue.js", "Nuxt.js", "React", "Next.js", "Svelte", "TypeScript", "JavaScript", "TailwindCSS", "HTML5", "Markdown"],
              
            ),
            SkillData(
                category="Backend Development",
                skills=["Python", "Django", "FastAPI", "Flask", "Next.js", "Nuxt.js", "PHP", "Laravel", "Express", "GraphQL", "REST API"],
          
            ),
            SkillData(
                category="Mobile Development",
                skills=["React Native", "NestJS", "Appwrite"],
            
            ),
            SkillData(
                category="Database & Storage",
                skills=["PostgreSQL", "MongoDB", "Redis", "Prisma", "MySQL", "SQLite", "Supabase", "Firebase"],
          
            ),
            SkillData(
                category="DevOps & Cloud",
                skills=["Docker", "Kubernetes", "AWS", "GitHub", "GitLab", "Jenkins", "Nginx", "Linux"],
           
            ),
            SkillData(
                category="AI & Machine Learning",
                skills=["TensorFlow", "PyTorch", "LangChain", "OpenAI", "Hugging Face", "scikit-learn", "CUDA", "Jupyter"],
           
            ),
            SkillData(
                category="Testing & API Tools",
                skills=["Postman", "Curl", "Swagger", "Pytest"],
            
            ),
            SkillData(
                category="Tools & Others",
                skills=["Git", "VS Code", "MicroPython", "Arduino", "Vim", "Bash", "WebRTC"],
           
            )
        ]
        
        # Education data
        self.education = [
            EducationData(
                institution="United International University (UIU)",
                degree="Bachelor of Science",
                field="Computer Science and Engineering",
                year="2020-2025",
                description="Specialized in Software Engineering."
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
                company="Amar Fuel",
                position="Software Engineer",
                duration="2023 - Present",
                description="Developing backend and automation systems at AmarFuel — a startup pioneering Bangladesh's first self-service fuel station solution using IoT and cloud technologies",
                technologies=["Python", "FastAPI", "IoT", "Postgresql", "PostgreSQL"]
            ),
            ExperienceData(
                company="Fiverr",
                position="Full Stack Developer (Freelance)",
                duration="2024 - Present",
                description="Delivered full-stack web solutions for global clients, building responsive interfaces and scalable backend systems to meet diverse business needs",
                technologies=["Vue.js", "Nuxt.js", "Python", "FastAPI", "Firebase", "PostgreSQL"]
            )
        ]
        
        # Achievements data
        self.achievements = [
            AchievementData(
                title="Finalist – National Project Showcase, UIU CSE Fest",
                description="Selected as a finalist in the national-level project showcase at UIU CSE Fest — recognized among top student innovators for presenting a solution-driven tech project demonstrating strong concept, execution and real-world relevance.",
                date="2024",
                link="https://example.com/uiu-cse-fest"
            ),
            AchievementData(
                title="Champion - UIU CSE Project Show, Fall 2023",
                description="Won first place in the UIU CSE Project Show Fall 2023 for outstanding project innovation and technical excellence",
                date="2023",
                link="https://example.com/uiu-champion"
            ),
            AchievementData(
                title="Finalist - National Project Showcase, Inventious 4.1, MIST",
                description="Selected as finalist in the national-level project showcase at Inventious 4.1, MIST for innovative technology solution",
                date="2024",
                link="https://example.com/inventious-mist"
            ),
            AchievementData(
                title="Finalist - National Project Showcase, Hult Prize Bangladesh 2025",
                description="Recognized as finalist in Hult Prize Bangladesh 2025 for social entrepreneurship and innovative business solution",
                date="2024",
                link="https://example.com/hult-prize"
            ),
            AchievementData(
                title="Google IT Support Professional Certificate",
                description="Completed Google IT Support Professional Certificate program, demonstrating proficiency in troubleshooting, customer service, networking, operating systems, system administration and security",
                date="2024",
                link="https://example.com/google-cert"
            )
        ]
        
        # Contact data
        self.contact = ContactData(
            email="ariffaysal.nayem@gmail.com",
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
