import streamlit as st
from professional.database import (
    get_roadmap_tasks_status,
    update_roadmap_task_status
)

# ──────────────────────────────────────────────────────────────
# Job Types → Courses mapping
# ──────────────────────────────────────────────────────────────
JOB_CATEGORIES = {
    "🖥️ IT / Software Development": {
        "icon": "🖥️",
        "courses": {
            "Python Full Stack Development": {
                "months": [
                    {
                        "focus": "Python Fundamentals & Backend Basics",
                        "tasks": [
                            "Master Python data structures, OOP, and error handling",
                            "Learn Django/Flask framework — build CRUD REST APIs",
                            "Set up PostgreSQL database and write ORM queries",
                            "Build a portfolio project: Task Management API"
                        ]
                    },
                    {
                        "focus": "Frontend & Full Stack Integration",
                        "tasks": [
                            "Learn HTML5, CSS3, and JavaScript ES6 fundamentals",
                            "Build responsive UI with React or Vue.js",
                            "Connect frontend to your Django REST backend",
                            "Add user authentication (JWT/OAuth)"
                        ]
                    },
                    {
                        "focus": "Deployment & Job Readiness",
                        "tasks": [
                            "Containerize your app with Docker",
                            "Deploy to AWS/Heroku with CI/CD pipeline",
                            "Build and polish 2 full-stack portfolio projects",
                            "Prepare resume, GitHub profile, and practice interviews"
                        ]
                    }
                ]
            },
            "Java Enterprise Development": {
                "months": [
                    {
                        "focus": "Core Java & Spring Boot Basics",
                        "tasks": [
                            "Master Java syntax, collections, streams, and OOP",
                            "Learn Spring Boot — create REST API with CRUD operations",
                            "Set up MySQL/PostgreSQL with JPA/Hibernate",
                            "Write unit tests with JUnit and Mockito"
                        ]
                    },
                    {
                        "focus": "Microservices & Advanced Spring",
                        "tasks": [
                            "Build microservices architecture with Spring Cloud",
                            "Implement API Gateway, service discovery (Eureka)",
                            "Add security with Spring Security and JWT",
                            "Set up message queues with RabbitMQ/Kafka"
                        ]
                    },
                    {
                        "focus": "Deployment & Enterprise Patterns",
                        "tasks": [
                            "Containerize services with Docker Compose",
                            "Deploy to AWS ECS or Kubernetes cluster",
                            "Implement logging, monitoring with ELK Stack",
                            "Build a capstone enterprise project and prepare for interviews"
                        ]
                    }
                ]
            },
            "Cloud Computing & AWS": {
                "months": [
                    {
                        "focus": "Cloud Foundations & AWS Core Services",
                        "tasks": [
                            "Study cloud computing concepts (IaaS, PaaS, SaaS)",
                            "Learn AWS IAM, EC2, S3, and VPC networking",
                            "Set up a multi-tier web app on AWS",
                            "Prepare for AWS Cloud Practitioner exam"
                        ]
                    },
                    {
                        "focus": "AWS Architecture & DevOps",
                        "tasks": [
                            "Master RDS, DynamoDB, and Lambda (serverless)",
                            "Build CI/CD pipelines with AWS CodePipeline",
                            "Learn CloudFormation / Terraform for IaC",
                            "Study high availability and auto-scaling patterns"
                        ]
                    },
                    {
                        "focus": "Advanced AWS & Certification",
                        "tasks": [
                            "Design fault-tolerant, scalable architectures",
                            "Implement monitoring with CloudWatch and X-Ray",
                            "Complete 3 AWS practice exams",
                            "Attempt AWS Solutions Architect Associate exam"
                        ]
                    }
                ]
            },
            "DevOps & CI/CD Engineering": {
                "months": [
                    {
                        "focus": "Linux, Git & Scripting Basics",
                        "tasks": [
                            "Master Linux commands, shell scripting (Bash)",
                            "Learn Git workflows — branching, merging, rebasing",
                            "Set up Jenkins/GitHub Actions for basic CI pipelines",
                            "Understand networking basics (DNS, TCP/IP, HTTP)"
                        ]
                    },
                    {
                        "focus": "Containers & Orchestration",
                        "tasks": [
                            "Learn Docker — build, run, and push images",
                            "Master Docker Compose for multi-container apps",
                            "Set up Kubernetes cluster (Minikube/K3s)",
                            "Deploy microservices to Kubernetes with Helm charts"
                        ]
                    },
                    {
                        "focus": "Infrastructure as Code & Monitoring",
                        "tasks": [
                            "Learn Terraform for infrastructure provisioning",
                            "Set up monitoring with Prometheus and Grafana",
                            "Implement centralized logging (ELK/Loki)",
                            "Build end-to-end CI/CD pipeline for a real project"
                        ]
                    }
                ]
            },
            "Frontend Development (React)": {
                "months": [
                    {
                        "focus": "HTML, CSS & JavaScript Mastery",
                        "tasks": [
                            "Master HTML5 semantic elements and CSS3 (Flexbox, Grid)",
                            "Learn JavaScript ES6+ — async/await, closures, modules",
                            "Build 3 responsive landing pages from scratch",
                            "Learn version control with Git and GitHub"
                        ]
                    },
                    {
                        "focus": "React.js Core & State Management",
                        "tasks": [
                            "Learn React components, props, hooks (useState, useEffect)",
                            "Master React Router for multi-page apps",
                            "Implement state management with Redux/Context API",
                            "Build a full React dashboard project"
                        ]
                    },
                    {
                        "focus": "Advanced React & Deployment",
                        "tasks": [
                            "Learn Next.js for SSR and static site generation",
                            "Add API integration with Axios/React Query",
                            "Write tests with Jest and React Testing Library",
                            "Deploy projects to Vercel/Netlify and polish portfolio"
                        ]
                    }
                ]
            }
        }
    },
    "📊 Data Science & Analytics": {
        "icon": "📊",
        "courses": {
            "Data Analysis with Python": {
                "months": [
                    {
                        "focus": "Python & Data Manipulation",
                        "tasks": [
                            "Learn Python basics — loops, functions, file handling",
                            "Master NumPy for numerical computing",
                            "Learn Pandas for data cleaning and transformation",
                            "Analyze 3 real-world datasets (Kaggle)"
                        ]
                    },
                    {
                        "focus": "Data Visualization & Statistics",
                        "tasks": [
                            "Master Matplotlib and Seaborn for visualizations",
                            "Learn descriptive & inferential statistics",
                            "Build interactive dashboards with Plotly",
                            "Complete an end-to-end EDA project"
                        ]
                    },
                    {
                        "focus": "SQL, BI Tools & Portfolio",
                        "tasks": [
                            "Master SQL queries — joins, subqueries, window functions",
                            "Learn Power BI or Tableau for business dashboards",
                            "Build 2 portfolio-ready data analysis projects",
                            "Prepare resume and practice case study interviews"
                        ]
                    }
                ]
            },
            "Machine Learning": {
                "months": [
                    {
                        "focus": "Math Foundations & Scikit-Learn",
                        "tasks": [
                            "Revise linear algebra, probability, and calculus basics",
                            "Learn supervised learning — regression and classification",
                            "Master Scikit-Learn pipeline (train/test, cross-validation)",
                            "Build 2 ML models on real datasets"
                        ]
                    },
                    {
                        "focus": "Advanced ML & Feature Engineering",
                        "tasks": [
                            "Learn ensemble methods (Random Forest, XGBoost, LightGBM)",
                            "Master feature engineering and selection techniques",
                            "Study unsupervised learning — clustering, PCA",
                            "Participate in a Kaggle competition"
                        ]
                    },
                    {
                        "focus": "Deep Learning & Deployment",
                        "tasks": [
                            "Learn neural networks with TensorFlow/PyTorch",
                            "Build a CNN for image classification",
                            "Deploy ML models as REST APIs with Flask/FastAPI",
                            "Create a capstone ML project for portfolio"
                        ]
                    }
                ]
            },
            "Business Intelligence & SQL": {
                "months": [
                    {
                        "focus": "SQL Fundamentals & Database Design",
                        "tasks": [
                            "Learn SQL basics — SELECT, WHERE, GROUP BY, HAVING",
                            "Master JOINs, subqueries, and CTEs",
                            "Understand database normalization and schema design",
                            "Practice with 50+ SQL problems on LeetCode/HackerRank"
                        ]
                    },
                    {
                        "focus": "Advanced SQL & Data Warehousing",
                        "tasks": [
                            "Learn window functions and analytical queries",
                            "Study data warehousing concepts (Star/Snowflake schema)",
                            "Learn ETL pipelines with Python or SQL tools",
                            "Work with BigQuery or Snowflake cloud data warehouse"
                        ]
                    },
                    {
                        "focus": "BI Dashboards & Reporting",
                        "tasks": [
                            "Master Power BI — DAX formulas, relationships, visuals",
                            "Build 3 interactive business dashboards",
                            "Learn Tableau for executive reporting",
                            "Create a BI portfolio and prepare for analyst interviews"
                        ]
                    }
                ]
            },
            "Data Engineering": {
                "months": [
                    {
                        "focus": "Python, SQL & Data Pipelines",
                        "tasks": [
                            "Master Python scripting for data processing",
                            "Learn advanced SQL and database optimization",
                            "Build ETL pipelines with Apache Airflow",
                            "Understand data formats — JSON, Parquet, Avro"
                        ]
                    },
                    {
                        "focus": "Big Data & Cloud Storage",
                        "tasks": [
                            "Learn Apache Spark for distributed data processing",
                            "Set up data lakes on AWS S3 / GCS",
                            "Master Kafka for real-time data streaming",
                            "Build a batch + streaming data pipeline"
                        ]
                    },
                    {
                        "focus": "Cloud Data Platforms & Portfolio",
                        "tasks": [
                            "Learn AWS Glue, Redshift, or GCP BigQuery",
                            "Implement data quality checks and monitoring",
                            "Build an end-to-end data engineering project",
                            "Prepare for Data Engineer interviews"
                        ]
                    }
                ]
            }
        }
    },
    "🎨 UI/UX Design": {
        "icon": "🎨",
        "courses": {
            "UI Design with Figma": {
                "months": [
                    {
                        "focus": "Design Principles & Figma Basics",
                        "tasks": [
                            "Study color theory, typography, and visual hierarchy",
                            "Learn Figma workspace — frames, components, auto-layout",
                            "Recreate 3 popular app screens in Figma",
                            "Build a personal design system (colors, fonts, spacing)"
                        ]
                    },
                    {
                        "focus": "Prototyping & Component Libraries",
                        "tasks": [
                            "Create interactive prototypes with Figma animations",
                            "Build reusable component libraries with variants",
                            "Design a complete mobile app (5+ screens)",
                            "Learn responsive design for web and mobile"
                        ]
                    },
                    {
                        "focus": "Portfolio & Handoff",
                        "tasks": [
                            "Learn design handoff with Figma Dev Mode",
                            "Study accessibility standards (WCAG)",
                            "Build 3 portfolio case studies with process documentation",
                            "Create a Dribbble/Behance portfolio"
                        ]
                    }
                ]
            },
            "UX Research & Strategy": {
                "months": [
                    {
                        "focus": "UX Fundamentals & Research Methods",
                        "tasks": [
                            "Study UX design principles and user-centered design",
                            "Learn research methods — interviews, surveys, card sorting",
                            "Conduct 5 user interviews for a sample product",
                            "Create user personas and journey maps"
                        ]
                    },
                    {
                        "focus": "Wireframing & Usability Testing",
                        "tasks": [
                            "Build low-fidelity wireframes for 2 products",
                            "Conduct usability tests and document findings",
                            "Learn information architecture and navigation design",
                            "Create a UX case study with research findings"
                        ]
                    },
                    {
                        "focus": "UX Strategy & Portfolio",
                        "tasks": [
                            "Study UX metrics — NPS, SUS, task success rate",
                            "Learn design thinking and workshop facilitation",
                            "Build 2 end-to-end UX case studies",
                            "Prepare UX portfolio and practice whiteboard exercises"
                        ]
                    }
                ]
            },
            "Web Design & CSS": {
                "months": [
                    {
                        "focus": "HTML & CSS Foundations",
                        "tasks": [
                            "Master HTML5 structure and semantic elements",
                            "Learn CSS — selectors, box model, positioning",
                            "Master Flexbox and CSS Grid layouts",
                            "Build 3 responsive web pages from designs"
                        ]
                    },
                    {
                        "focus": "Advanced CSS & Animations",
                        "tasks": [
                            "Learn CSS animations, transitions, and keyframes",
                            "Study modern CSS — variables, container queries",
                            "Build a responsive portfolio website",
                            "Learn Tailwind CSS or Bootstrap framework"
                        ]
                    },
                    {
                        "focus": "JavaScript Basics & Deployment",
                        "tasks": [
                            "Learn JavaScript for interactive web elements",
                            "Build a dynamic landing page with scroll animations",
                            "Deploy websites to Netlify or GitHub Pages",
                            "Create 3 web design portfolio projects"
                        ]
                    }
                ]
            }
        }
    },
    "📱 Mobile App Development": {
        "icon": "📱",
        "courses": {
            "Android Development (Kotlin)": {
                "months": [
                    {
                        "focus": "Kotlin & Android Studio Setup",
                        "tasks": [
                            "Learn Kotlin syntax — null safety, coroutines, extensions",
                            "Set up Android Studio and understand project structure",
                            "Build UI with Jetpack Compose or XML layouts",
                            "Create a simple calculator and notes app"
                        ]
                    },
                    {
                        "focus": "Architecture & Data Storage",
                        "tasks": [
                            "Learn MVVM architecture with ViewModel and LiveData",
                            "Master Room database for local storage",
                            "Implement Retrofit for REST API calls",
                            "Build a weather app with API integration"
                        ]
                    },
                    {
                        "focus": "Advanced Features & Publishing",
                        "tasks": [
                            "Add Firebase authentication and Cloud Firestore",
                            "Implement push notifications and background services",
                            "Build a full-featured app (e.g., task manager or e-commerce)",
                            "Publish your app on Google Play Store"
                        ]
                    }
                ]
            },
            "iOS Development (Swift)": {
                "months": [
                    {
                        "focus": "Swift & Xcode Fundamentals",
                        "tasks": [
                            "Learn Swift syntax — optionals, closures, protocols",
                            "Set up Xcode and understand iOS project structure",
                            "Build UI with SwiftUI framework",
                            "Create 2 simple iOS apps (calculator, to-do list)"
                        ]
                    },
                    {
                        "focus": "Data, Networking & Architecture",
                        "tasks": [
                            "Learn Core Data for local persistence",
                            "Implement URLSession/Alamofire for API calls",
                            "Master MVVM architecture pattern",
                            "Build a news reader app with API integration"
                        ]
                    },
                    {
                        "focus": "Advanced iOS & App Store",
                        "tasks": [
                            "Add Firebase/CloudKit backend integration",
                            "Implement push notifications and widgets",
                            "Build a polished portfolio app",
                            "Submit your app to the App Store"
                        ]
                    }
                ]
            },
            "Flutter Cross-Platform Development": {
                "months": [
                    {
                        "focus": "Dart & Flutter Basics",
                        "tasks": [
                            "Learn Dart language — async, streams, null safety",
                            "Set up Flutter and understand widget tree",
                            "Master Material Design widgets and layouts",
                            "Build 2 basic Flutter apps"
                        ]
                    },
                    {
                        "focus": "State Management & APIs",
                        "tasks": [
                            "Learn state management (Provider/Riverpod/BLoC)",
                            "Implement REST API calls with Dio/HTTP packages",
                            "Master navigation and routing in Flutter",
                            "Build a recipe app with API and local storage"
                        ]
                    },
                    {
                        "focus": "Firebase, Testing & Publishing",
                        "tasks": [
                            "Integrate Firebase Auth, Firestore, and Storage",
                            "Write widget and integration tests",
                            "Build a production-ready cross-platform app",
                            "Publish to Google Play and App Store"
                        ]
                    }
                ]
            },
            "React Native Development": {
                "months": [
                    {
                        "focus": "JavaScript & React Native Setup",
                        "tasks": [
                            "Master JavaScript ES6+ and React fundamentals",
                            "Set up React Native with Expo CLI",
                            "Learn core components — View, Text, ScrollView, FlatList",
                            "Build 2 starter apps with navigation"
                        ]
                    },
                    {
                        "focus": "State, APIs & Native Modules",
                        "tasks": [
                            "Implement state management with Redux/Context",
                            "Master API integration with Axios",
                            "Learn AsyncStorage and SQLite for local data",
                            "Build a social media feed app"
                        ]
                    },
                    {
                        "focus": "Advanced Features & Deployment",
                        "tasks": [
                            "Add push notifications with Firebase/Expo",
                            "Implement maps, camera, and device APIs",
                            "Build a complete production app",
                            "Deploy to both app stores"
                        ]
                    }
                ]
            }
        }
    },
    "🔒 Cybersecurity": {
        "icon": "🔒",
        "courses": {
            "Ethical Hacking & Penetration Testing": {
                "months": [
                    {
                        "focus": "Networking & Security Fundamentals",
                        "tasks": [
                            "Study TCP/IP, DNS, HTTP/S, and OSI model",
                            "Learn Linux command line and Bash scripting",
                            "Set up Kali Linux and VirtualBox lab environment",
                            "Study OWASP Top 10 web vulnerabilities"
                        ]
                    },
                    {
                        "focus": "Scanning, Exploitation & Tools",
                        "tasks": [
                            "Master Nmap for network scanning and enumeration",
                            "Learn Burp Suite for web app testing",
                            "Practice exploitation with Metasploit framework",
                            "Complete 10 challenges on TryHackMe/HackTheBox"
                        ]
                    },
                    {
                        "focus": "Advanced Pentesting & Certification",
                        "tasks": [
                            "Learn privilege escalation techniques (Linux & Windows)",
                            "Study Active Directory attacks and defense",
                            "Write professional penetration testing reports",
                            "Prepare for CEH or CompTIA PenTest+ certification"
                        ]
                    }
                ]
            },
            "SOC Analyst & Threat Detection": {
                "months": [
                    {
                        "focus": "Security Operations Fundamentals",
                        "tasks": [
                            "Study cybersecurity frameworks (NIST, MITRE ATT&CK)",
                            "Learn log analysis and SIEM basics (Splunk/ELK)",
                            "Understand incident response lifecycle",
                            "Study common attack vectors and IOCs"
                        ]
                    },
                    {
                        "focus": "Threat Hunting & SIEM Mastery",
                        "tasks": [
                            "Master Splunk searches, dashboards, and alerts",
                            "Learn threat intelligence feeds and correlation",
                            "Practice analyzing malware and phishing samples",
                            "Complete SOC simulation labs"
                        ]
                    },
                    {
                        "focus": "Incident Response & Certification",
                        "tasks": [
                            "Build incident response playbooks",
                            "Learn digital forensics basics",
                            "Practice end-to-end incident investigation",
                            "Prepare for CompTIA Security+ or CySA+ exam"
                        ]
                    }
                ]
            },
            "Network Security & Firewall Administration": {
                "months": [
                    {
                        "focus": "Networking Deep Dive",
                        "tasks": [
                            "Master subnetting, VLANs, and routing protocols",
                            "Learn firewall concepts and ACL configuration",
                            "Set up pfSense/iptables in a lab environment",
                            "Study VPN technologies (IPSec, SSL/TLS)"
                        ]
                    },
                    {
                        "focus": "Firewall & IDS/IPS Configuration",
                        "tasks": [
                            "Configure enterprise firewall rules and policies",
                            "Set up Snort/Suricata IDS/IPS",
                            "Learn network segmentation and zero trust",
                            "Implement network monitoring with Wireshark"
                        ]
                    },
                    {
                        "focus": "Hardening & Compliance",
                        "tasks": [
                            "Learn server and endpoint hardening techniques",
                            "Study compliance frameworks (PCI-DSS, HIPAA, ISO 27001)",
                            "Build a network security architecture project",
                            "Prepare for CCNA Security or CompTIA Network+ exam"
                        ]
                    }
                ]
            }
        }
    },
    "🏫 Teaching / Education": {
        "icon": "🏫",
        "courses": {
            "Online Course Creation & EdTech": {
                "months": [
                    {
                        "focus": "Course Design & Instructional Strategy",
                        "tasks": [
                            "Study instructional design models (ADDIE, Bloom's Taxonomy)",
                            "Define your course topic, audience, and learning outcomes",
                            "Create a detailed course outline with module breakdowns",
                            "Write scripts for the first 5 video lessons"
                        ]
                    },
                    {
                        "focus": "Content Production & Platform Setup",
                        "tasks": [
                            "Learn video recording and editing (OBS, Camtasia, DaVinci)",
                            "Record and edit first 10 lessons",
                            "Create quizzes, assignments, and downloadable resources",
                            "Set up course on Udemy / Teachable / YouTube"
                        ]
                    },
                    {
                        "focus": "Launch, Marketing & Student Engagement",
                        "tasks": [
                            "Write compelling course descriptions and landing pages",
                            "Set up email marketing and social media promotion",
                            "Launch course and collect initial student feedback",
                            "Iterate based on reviews and add bonus content"
                        ]
                    }
                ]
            },
            "Classroom Teaching & Pedagogy": {
                "months": [
                    {
                        "focus": "Teaching Fundamentals & Lesson Planning",
                        "tasks": [
                            "Study modern pedagogy — constructivism, differentiated instruction",
                            "Learn lesson planning with clear objectives and assessments",
                            "Explore classroom management strategies",
                            "Observe and document 5 teaching sessions (online or in-person)"
                        ]
                    },
                    {
                        "focus": "Teaching Tools & Assessment Design",
                        "tasks": [
                            "Learn Google Classroom, Canva, Kahoot, and Quizlet",
                            "Create formative and summative assessments",
                            "Design interactive activities and group projects",
                            "Practice teach 3 sessions and collect peer feedback"
                        ]
                    },
                    {
                        "focus": "Advanced Techniques & Professional Growth",
                        "tasks": [
                            "Study inclusive teaching and special education basics",
                            "Build a teaching portfolio with lesson plans and reflections",
                            "Attend 2 education webinars or workshops",
                            "Apply for teaching positions or volunteer teaching roles"
                        ]
                    }
                ]
            },
            "Corporate Training & L&D": {
                "months": [
                    {
                        "focus": "Training Needs Analysis & Design",
                        "tasks": [
                            "Learn Training Needs Analysis (TNA) methodology",
                            "Study adult learning principles (Andragogy)",
                            "Design a training program for a sample corporate topic",
                            "Create training materials — slides, handouts, activities"
                        ]
                    },
                    {
                        "focus": "Facilitation & Delivery Skills",
                        "tasks": [
                            "Master facilitation techniques for workshops",
                            "Learn to use Zoom, Teams, and Miro for virtual training",
                            "Practice delivering 3 training sessions",
                            "Collect and analyze participant feedback"
                        ]
                    },
                    {
                        "focus": "Evaluation & LMS Management",
                        "tasks": [
                            "Study Kirkpatrick's 4-level evaluation model",
                            "Learn LMS platforms (Moodle, SAP Litmos, TalentLMS)",
                            "Build a complete L&D program with evaluation metrics",
                            "Prepare resume targeting L&D / Training Manager roles"
                        ]
                    }
                ]
            }
        }
    },
    "📈 Digital Marketing": {
        "icon": "📈",
        "courses": {
            "SEO & Content Marketing": {
                "months": [
                    {
                        "focus": "SEO Fundamentals & Keyword Research",
                        "tasks": [
                            "Study how search engines work (crawling, indexing, ranking)",
                            "Master keyword research with Ahrefs/SEMrush/Ubersuggest",
                            "Learn on-page SEO — meta tags, headings, internal linking",
                            "Audit 2 websites for SEO improvements"
                        ]
                    },
                    {
                        "focus": "Content Strategy & Creation",
                        "tasks": [
                            "Build a content calendar with topic clusters",
                            "Write 8 SEO-optimized blog posts",
                            "Learn content repurposing — blogs to social, video, infographics",
                            "Study technical SEO — site speed, schema markup, sitemaps"
                        ]
                    },
                    {
                        "focus": "Analytics & Link Building",
                        "tasks": [
                            "Master Google Analytics 4 and Search Console",
                            "Learn link building strategies — guest posts, outreach",
                            "Track rankings and organic traffic growth",
                            "Build a content marketing case study for portfolio"
                        ]
                    }
                ]
            },
            "Social Media Marketing": {
                "months": [
                    {
                        "focus": "Platform Strategy & Content Planning",
                        "tasks": [
                            "Study platform algorithms — Instagram, LinkedIn, YouTube, X",
                            "Define brand voice, target audience, and content pillars",
                            "Create a 30-day content calendar",
                            "Learn Canva for social media graphics"
                        ]
                    },
                    {
                        "focus": "Content Creation & Community Building",
                        "tasks": [
                            "Create and schedule 30 posts across 2 platforms",
                            "Learn video editing for Reels/Shorts (CapCut/Premiere)",
                            "Study community engagement and growth hacking tactics",
                            "Analyze competitors and benchmark metrics"
                        ]
                    },
                    {
                        "focus": "Paid Ads & Analytics",
                        "tasks": [
                            "Learn Meta Ads Manager for Facebook/Instagram campaigns",
                            "Set up ad campaigns with A/B testing",
                            "Master social media analytics and reporting",
                            "Build a social media marketing portfolio with results"
                        ]
                    }
                ]
            },
            "Google Ads & PPC Advertising": {
                "months": [
                    {
                        "focus": "PPC Fundamentals & Google Ads Setup",
                        "tasks": [
                            "Study PPC advertising concepts — CPC, CTR, Quality Score",
                            "Set up Google Ads account and link Analytics",
                            "Learn campaign types — Search, Display, Shopping, Video",
                            "Create your first search campaign with keyword targeting"
                        ]
                    },
                    {
                        "focus": "Campaign Optimization & Bidding",
                        "tasks": [
                            "Master bidding strategies — manual CPC, target CPA, ROAS",
                            "Learn ad copywriting and extension best practices",
                            "Set up conversion tracking and remarketing audiences",
                            "Optimize campaigns with A/B testing and negative keywords"
                        ]
                    },
                    {
                        "focus": "Advanced PPC & Certification",
                        "tasks": [
                            "Learn Display and YouTube video ad campaigns",
                            "Master Google Ads scripts and automation rules",
                            "Build PPC case studies with ROI analysis",
                            "Prepare for Google Ads Certification exam"
                        ]
                    }
                ]
            },
            "Email Marketing & Automation": {
                "months": [
                    {
                        "focus": "Email Fundamentals & List Building",
                        "tasks": [
                            "Study email marketing best practices and regulations (CAN-SPAM, GDPR)",
                            "Set up Mailchimp/ConvertKit/Brevo account",
                            "Create lead magnets and opt-in forms",
                            "Build your first email list with 100+ subscribers"
                        ]
                    },
                    {
                        "focus": "Campaign Design & Copywriting",
                        "tasks": [
                            "Learn email copywriting — subject lines, CTAs, storytelling",
                            "Design responsive email templates",
                            "Create welcome sequence and nurture campaigns",
                            "A/B test subject lines and send times"
                        ]
                    },
                    {
                        "focus": "Automation & Analytics",
                        "tasks": [
                            "Build automated workflows — abandoned cart, re-engagement",
                            "Master segmentation and personalization",
                            "Track KPIs — open rate, click rate, conversion rate",
                            "Create an email marketing portfolio with metrics"
                        ]
                    }
                ]
            }
        }
    },
    "💼 Business & Management": {
        "icon": "💼",
        "courses": {
            "Project Management (PMP/Agile)": {
                "months": [
                    {
                        "focus": "PM Fundamentals & Waterfall",
                        "tasks": [
                            "Study project management life cycle and knowledge areas",
                            "Learn WBS, Gantt charts, and critical path method",
                            "Master stakeholder and risk management",
                            "Create a project plan for a sample project"
                        ]
                    },
                    {
                        "focus": "Agile & Scrum Framework",
                        "tasks": [
                            "Study Agile Manifesto and Scrum framework",
                            "Learn sprint planning, daily standups, retrospectives",
                            "Master Jira/Trello for project tracking",
                            "Run a simulated 2-week sprint with a team"
                        ]
                    },
                    {
                        "focus": "Advanced PM & Certification",
                        "tasks": [
                            "Study hybrid project management approaches",
                            "Learn earned value management and project metrics",
                            "Complete PMP/CAPM or PSM I practice exams",
                            "Prepare for certification and build PM portfolio"
                        ]
                    }
                ]
            },
            "Business Analysis": {
                "months": [
                    {
                        "focus": "BA Fundamentals & Requirements",
                        "tasks": [
                            "Study BABOK knowledge areas and techniques",
                            "Learn requirements elicitation — interviews, workshops",
                            "Master BRD, FRD, and user story writing",
                            "Create a requirements document for a sample project"
                        ]
                    },
                    {
                        "focus": "Process Modeling & Data Analysis",
                        "tasks": [
                            "Learn BPMN process modeling and flowcharting",
                            "Master use case diagrams and activity diagrams",
                            "Study data analysis for business insights (Excel/SQL)",
                            "Document as-is and to-be process flows"
                        ]
                    },
                    {
                        "focus": "Stakeholder Management & Portfolio",
                        "tasks": [
                            "Learn stakeholder analysis and communication planning",
                            "Study change management frameworks",
                            "Build 2 BA case studies with deliverables",
                            "Prepare for CBAP/ECBA certification"
                        ]
                    }
                ]
            },
            "Product Management": {
                "months": [
                    {
                        "focus": "Product Strategy & Discovery",
                        "tasks": [
                            "Study product management frameworks (Lean, Jobs-to-be-Done)",
                            "Learn market research and competitive analysis",
                            "Define product vision, strategy, and success metrics",
                            "Create user personas and problem statements"
                        ]
                    },
                    {
                        "focus": "Roadmapping & Execution",
                        "tasks": [
                            "Master product roadmapping tools (ProductBoard, Aha!)",
                            "Learn prioritization frameworks (RICE, MoSCoW, Kano)",
                            "Write PRDs and user stories with acceptance criteria",
                            "Work with engineering teams on sprint planning"
                        ]
                    },
                    {
                        "focus": "Growth, Analytics & Portfolio",
                        "tasks": [
                            "Study product analytics (Amplitude, Mixpanel, GA4)",
                            "Learn growth metrics — retention, activation, referral",
                            "Build a product case study with data-driven decisions",
                            "Prepare for PM interviews — CIRCLES, estimation questions"
                        ]
                    }
                ]
            }
        }
    },
    "🏥 Healthcare IT": {
        "icon": "🏥",
        "courses": {
            "Health Informatics": {
                "months": [
                    {
                        "focus": "Healthcare Systems & Data Standards",
                        "tasks": [
                            "Study healthcare IT landscape — EHR, EMR, PHR systems",
                            "Learn HL7 FHIR and healthcare data standards",
                            "Understand HIPAA compliance and patient data security",
                            "Explore popular EHR systems (Epic, Cerner, MEDITECH)"
                        ]
                    },
                    {
                        "focus": "Clinical Data Analysis & Reporting",
                        "tasks": [
                            "Learn clinical data analysis with Python/SQL",
                            "Study healthcare KPIs and quality metrics",
                            "Build dashboards for clinical outcomes reporting",
                            "Practice with open healthcare datasets (MIMIC, CMS)"
                        ]
                    },
                    {
                        "focus": "Interoperability & Certification",
                        "tasks": [
                            "Study system interoperability and HIE (Health Info Exchange)",
                            "Learn telemedicine platforms and digital health tools",
                            "Build a health informatics capstone project",
                            "Prepare for CAHIMS or CPHIMS certification"
                        ]
                    }
                ]
            },
            "Medical Coding & Billing": {
                "months": [
                    {
                        "focus": "Medical Terminology & Anatomy Basics",
                        "tasks": [
                            "Study medical terminology — prefixes, suffixes, root words",
                            "Learn basic human anatomy and physiology systems",
                            "Understand healthcare settings and provider workflows",
                            "Complete medical terminology practice quizzes"
                        ]
                    },
                    {
                        "focus": "ICD-10, CPT & HCPCS Coding",
                        "tasks": [
                            "Master ICD-10-CM diagnosis coding guidelines",
                            "Learn CPT procedural coding for E&M and surgeries",
                            "Study HCPCS Level II codes for supplies and equipment",
                            "Practice coding 50+ clinical scenarios"
                        ]
                    },
                    {
                        "focus": "Billing, Revenue Cycle & Certification",
                        "tasks": [
                            "Learn revenue cycle management end-to-end",
                            "Study insurance claims, denials, and appeals process",
                            "Practice with medical billing software",
                            "Prepare for CPC (AAPC) or CCS (AHIMA) certification"
                        ]
                    }
                ]
            }
        }
    },
    "🎮 Game Development": {
        "icon": "🎮",
        "courses": {
            "Unity Game Development (C#)": {
                "months": [
                    {
                        "focus": "C# & Unity Fundamentals",
                        "tasks": [
                            "Learn C# basics — classes, inheritance, interfaces",
                            "Set up Unity and understand the editor, scenes, GameObjects",
                            "Master Unity physics, colliders, and rigidbodies",
                            "Build a 2D platformer game prototype"
                        ]
                    },
                    {
                        "focus": "3D Game Development & UI",
                        "tasks": [
                            "Learn 3D modeling basics and asset importing",
                            "Implement player controls, camera systems, and AI",
                            "Build UI with Unity Canvas — menus, HUD, health bars",
                            "Create a 3D adventure/shooter game prototype"
                        ]
                    },
                    {
                        "focus": "Polish, Multiplayer & Publishing",
                        "tasks": [
                            "Add audio, particle effects, and post-processing",
                            "Learn basic multiplayer with Unity Netcode",
                            "Optimize performance and build for target platform",
                            "Publish game on itch.io or Steam and build portfolio"
                        ]
                    }
                ]
            },
            "Unreal Engine Development": {
                "months": [
                    {
                        "focus": "Unreal Engine & Blueprint Basics",
                        "tasks": [
                            "Learn Unreal Engine editor and project structure",
                            "Master Blueprint visual scripting fundamentals",
                            "Study materials, lighting, and level design basics",
                            "Build a simple 3D environment walkthrough"
                        ]
                    },
                    {
                        "focus": "Gameplay Systems & C++",
                        "tasks": [
                            "Learn Unreal C++ basics and GameFramework classes",
                            "Implement character movement, combat, and inventory",
                            "Master Unreal UI with UMG widgets",
                            "Build a third-person action game prototype"
                        ]
                    },
                    {
                        "focus": "Advanced Features & Portfolio",
                        "tasks": [
                            "Add AI behavior trees for NPCs",
                            "Learn Niagara particle system and Sequencer cinematics",
                            "Optimize and package game for Windows/console",
                            "Create a game portfolio and demo reel"
                        ]
                    }
                ]
            },
            "Game Design & Theory": {
                "months": [
                    {
                        "focus": "Game Design Principles",
                        "tasks": [
                            "Study core game design concepts — MDA framework, game loops",
                            "Analyze 10 popular games — mechanics, dynamics, aesthetics",
                            "Learn level design principles and pacing",
                            "Create a Game Design Document (GDD) for an original game"
                        ]
                    },
                    {
                        "focus": "Prototyping & Playtesting",
                        "tasks": [
                            "Build paper prototypes and board game versions",
                            "Create a digital prototype in Unity/Godot",
                            "Conduct 5 playtesting sessions with feedback forms",
                            "Iterate on game mechanics based on playtest data"
                        ]
                    },
                    {
                        "focus": "Narrative Design & Portfolio",
                        "tasks": [
                            "Study narrative design — branching stories, world-building",
                            "Learn game balancing and economy design",
                            "Build a comprehensive game design portfolio",
                            "Prepare for game designer interviews and pitch presentations"
                        ]
                    }
                ]
            }
        }
    }
}


def render_roadmap_section(user_id):
    st.subheader("10. 90-Day Career Roadmap")
    st.caption("Select your career field and a course to get a personalized 90-day learning roadmap.")

    # ── Step 1: Job Type Selection ──
    job_types = list(JOB_CATEGORIES.keys())

    selected_job = st.selectbox(
        "**Step 1:** Select your career field",
        options=["-- Select a Career Field --"] + job_types,
        index=0,
        key="roadmap_job_type"
    )

    if selected_job == "-- Select a Career Field --":
        st.info("👆 Choose a career field above to see available courses and generate your roadmap.")
        return

    # ── Step 2: Course Selection ──
    category_data = JOB_CATEGORIES[selected_job]
    course_names = list(category_data["courses"].keys())

    selected_course = st.selectbox(
        "**Step 2:** Select a course / skill to learn",
        options=["-- Select a Course --"] + course_names,
        index=0,
        key="roadmap_course"
    )

    if selected_course == "-- Select a Course --":
        st.info("👆 Pick a course above to generate your personalized 90-day roadmap.")
        return

    st.divider()

    # ── Step 3: Display the Roadmap ──
    course_data = category_data["courses"][selected_course]
    months = course_data["months"]

    st.markdown(f"### 📋 Your 90-Day Roadmap")
    st.markdown(f"**Career Field:** {selected_job}  \n**Course:** {selected_course}")
    st.write("")

    # Load saved task states
    task_states = get_roadmap_tasks_status(user_id)

    total_tasks = 0
    completed_count = 0

    for i, month in enumerate(months, 1):
        with st.expander(f"📅 Month {i} — {month['focus']}", expanded=(i == 1)):
            for task in month["tasks"]:
                total_tasks += 1
                # Create a unique key combining job, course, month, and task
                t_key = f"{selected_job}|{selected_course}|Month{i}|{task}"
                is_done = task_states.get(t_key, False)
                checked = st.checkbox(task, value=is_done, key=f"rm_{i}_{task[:40]}")
                if checked != is_done:
                    update_roadmap_task_status(user_id, t_key, checked)
                    st.rerun()
                if checked:
                    completed_count += 1

    # ── Progress Bar ──
    st.write("")
    progress_pct = float(completed_count) / max(total_tasks, 1)
    st.markdown(f"**Roadmap Progress:** `{completed_count}/{total_tasks} tasks completed ({int(progress_pct * 100)}%)`")
    st.progress(progress_pct)

    if progress_pct >= 1.0:
        st.success("🎉 Congratulations! You've completed this 90-day roadmap! Consider exploring another course to continue growing.")
    elif progress_pct >= 0.5:
        st.info("💪 Great progress! You're over halfway through. Keep it up!")
