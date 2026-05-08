"""
Management command: python manage.py seed_data

Populates the database with default portfolio content.
Run once after migrations. Safe to re-run — skips existing data.
"""
from django.core.management.base import BaseCommand
from MainApp.models import Profile, Project, Skill, ResumeSection, PageContent


class Command(BaseCommand):
    help = 'Seed the database with default portfolio content'

    def handle(self, *args, **kwargs):
        self._seed_profile()
        self._seed_page_content()
        self._seed_projects()
        self._seed_skills()
        self._seed_resume()
        self.stdout.write(self.style.SUCCESS('\nSeed data loaded successfully!'))

    # ------------------------------------------------------------------ #
    def _seed_profile(self):
        if Profile.objects.exists():
            self.stdout.write('  Profile already exists — skipping.')
            return
        Profile.objects.create(
            name='Your Name',
            tagline='Full-Stack Developer | AI & Automation Specialist',
            bio=(
                'I am a passionate full-stack developer and AI enthusiast with a focus on building '
                'intelligent, real-world applications. I combine strong Python and Django skills with '
                'modern AI tools like LangChain, n8n, and Google AI Studio to deliver impactful solutions.\n\n'
                'I believe in clean code, great UX, and continuous learning. When I\'m not coding, '
                'I\'m exploring new AI workflows or contributing to open-source projects.\n\n'
                'I am currently open to full-time, contract, and freelance opportunities. '
                'Let\'s build something great together!'
            ),
            email='yourname@email.com',
            phone='+1 (555) 000-0000',
            location='City, Country',
            github='https://github.com/yourusername',
            linkedin='https://linkedin.com/in/yourusername',
            resume_summary=(
                'Results-driven Full-Stack Developer with experience in Python, Django, and AI/ML technologies. '
                'Proven track record of building scalable web applications and intelligent automation systems. '
                'Passionate about leveraging AI to solve complex problems and improve user experiences.'
            ),
        )
        self.stdout.write('  OK Profile created.')

    # ------------------------------------------------------------------ #
    def _seed_page_content(self):
        entries = [
            dict(page='home', section='hero', title='Welcome to My Portfolio',
                 body='I build full-stack web apps and AI-powered tools that make a difference.'),
            dict(page='about', section='values', title='What I Value',
                 body='Clean code, clear communication, continuous learning, and building things that actually help people.'),
            dict(page='about', section='interests', title='Outside of Code',
                 body='I enjoy exploring AI research, contributing to open source, and staying up to date with the latest in machine learning and developer tooling.'),
        ]
        created = 0
        for e in entries:
            _, was_created = PageContent.objects.get_or_create(
                page=e['page'], section=e['section'],
                defaults={'title': e['title'], 'body': e['body']},
            )
            if was_created:
                created += 1
        self.stdout.write(f'  OK {created} page content entries created.')

    # ------------------------------------------------------------------ #
    def _seed_projects(self):
        projects = [
            dict(
                title='Chatbot Project',
                short_description='A production-ready AI chatbot with multi-turn dialogue, session memory, and CRM integration.',
                description=(
                    'Built a full-stack AI chatbot platform using Python and Django, integrating OpenAI\'s API for '
                    'natural language understanding. Supports multi-turn conversations, session management via Redis, '
                    'and an admin dashboard for managing bot responses and analytics.'
                ),
                tools='Python, Django, OpenAI API, JavaScript, PostgreSQL, Redis',
                problem=(
                    'Businesses were overwhelmed by repetitive customer support queries. Existing enterprise chatbot '
                    'solutions were too expensive and rigid — they needed an intelligent, context-aware bot that could '
                    'integrate with their existing CRM without a six-figure price tag.'
                ),
                key_features=(
                    'Multi-turn conversation with full context memory\n'
                    'Redis-backed session management\n'
                    'Admin dashboard with response analytics\n'
                    'CRM integration via REST API\n'
                    'Fallback keyword engine for offline resilience\n'
                    'Rate limiting and abuse protection'
                ),
                role=(
                    'Sole developer — designed the full architecture, built the Django REST backend, integrated the '
                    'OpenAI API, implemented Redis session management, and delivered the JavaScript frontend UI.'
                ),
                solution=(
                    'Designed a modular chatbot framework using OpenAI for language understanding, Django for the '
                    'backend API, and Redis for session persistence. Built a clean JS frontend with typing indicators '
                    'and smooth animations. Added a local keyword fallback so the bot never goes silent.'
                ),
                challenge=(
                    'Maintaining coherent conversation context across HTTP requests without degrading performance. '
                    'Solved by serialising conversation history into Redis with TTL-based expiry.'
                ),
                learnings=(
                    'Prompt engineering for consistent tone, Redis pub/sub patterns, API rate limiting strategies, '
                    'and the importance of graceful fallback design in production AI systems.'
                ),
                outcome=(
                    'Reduced customer support response times by 60%, handling 500+ daily queries automatically. '
                    'Deployed to three clients within the first month, each with custom persona configurations.'
                ),
                order=1, is_featured=True,
            ),
            dict(
                title='n8n Agent Workflow Project',
                short_description='Automated complex business workflows with n8n — eliminating 15+ manual hours per week.',
                description=(
                    'Designed and implemented a comprehensive workflow automation system using n8n\'s visual '
                    'programming interface. Automates data ingestion, cross-platform syncing, notifications, '
                    'and weekly reporting across Slack, Google Sheets, Airtable, and custom APIs.'
                ),
                tools='n8n, Node.js, REST APIs, Google Workspace, Slack, Airtable, Webhooks',
                problem=(
                    'The operations team was spending 15+ hours every week on repetitive manual tasks: copying data '
                    'between systems, sending status notifications, generating reports, and chasing approvals — '
                    'all of which were error-prone and kept the team from strategic work.'
                ),
                key_features=(
                    'Webhook-triggered automation pipelines\n'
                    'Conditional logic and data routing\n'
                    'Automated Slack digest reports\n'
                    'Google Sheets and Airtable bi-directional sync\n'
                    'Error handling with retry logic and alerts\n'
                    'Version-controlled workflow documentation'
                ),
                role=(
                    'Workflow architect and sole implementer — mapped all manual processes, designed the automation '
                    'flows, built and tested every n8n workflow, and trained the team on monitoring and maintenance.'
                ),
                solution=(
                    'Built a network of n8n workflows triggered by webhooks and schedules. Used conditional nodes '
                    'for smart routing, HTTP request nodes for third-party API calls, and error-handling branches '
                    'to ensure reliability. All workflows are documented and version-controlled in Git.'
                ),
                challenge=(
                    'Handling API rate limits across multiple platforms simultaneously while ensuring data consistency. '
                    'Solved with queue-based execution, exponential backoff, and idempotency checks.'
                ),
                learnings=(
                    'n8n workflow design patterns, webhook security best practices, asynchronous processing, '
                    'and how to map messy real-world processes into clean automation logic.'
                ),
                outcome=(
                    'Eliminated 15+ hours of manual work per week. Error rates dropped 90%. The team redirected '
                    'that time entirely to strategic initiatives within the first two weeks of deployment.'
                ),
                order=2, is_featured=True,
            ),
            dict(
                title='LangChain Agent Project',
                short_description='An autonomous AI agent that researches, plans, and executes complex multi-step tasks end-to-end.',
                description=(
                    'Developed an autonomous AI agent using the LangChain framework, capable of decomposing complex '
                    'user queries into actionable steps, invoking tools like web search, PDF parsers, and code '
                    'executors, and iterating until the task is fully complete — with no human intervention.'
                ),
                tools='Python, LangChain, OpenAI GPT-4, FAISS, ChromaDB, FastAPI, Docker',
                problem=(
                    'Users needed an AI assistant that could handle deep research tasks end-to-end — not just '
                    'answer questions, but browse the web, read documents, run calculations, and synthesise '
                    'findings into a coherent report without requiring constant human prompting.'
                ),
                key_features=(
                    'ReAct reasoning loop (Reason + Act cycles)\n'
                    'Web search tool (DuckDuckGo integration)\n'
                    'PDF parsing and summarisation\n'
                    'Vector memory with ChromaDB / FAISS\n'
                    'Python code execution tool\n'
                    'Streaming responses via FastAPI\n'
                    'Docker containerisation for deployment'
                ),
                role=(
                    'AI engineer and architect — designed the ReAct agent loop, built all custom tools, '
                    'integrated ChromaDB for persistent memory, wrapped everything in a FastAPI service, '
                    'and containerised the system with Docker.'
                ),
                solution=(
                    'Built a ReAct-style agent with LangChain, giving it custom tools for web search, PDF reading, '
                    'vector search memory, and Python execution. Added streaming so responses appear in real time. '
                    'Deployed as a Dockerised FastAPI service for easy scaling.'
                ),
                challenge=(
                    'Preventing the agent from hallucinating tool results and getting stuck in reasoning loops. '
                    'Solved with strict output parsers, tool validation layers, and maximum iteration limits.'
                ),
                learnings=(
                    'LangChain agent architectures, vector database design, prompt chaining strategies, '
                    'streaming API responses, and how to make AI agents reliable in production.'
                ),
                outcome=(
                    'The agent handles complex multi-step research in minutes instead of hours. '
                    'Users reported a 10x productivity improvement on research-heavy tasks.'
                ),
                order=3, is_featured=True,
            ),
            dict(
                title='Google AI Studio Media Project',
                short_description='AI-powered document analysis and image recognition apps built with Google AI Studio and Gemini.',
                description=(
                    'Created a suite of AI applications using Google AI Studio and the Gemini model family. '
                    'Includes a document intelligence tool (upload, summarise, and query PDFs), an image '
                    'captioning and analysis API, and a multi-modal chatbot interface.'
                ),
                tools='Python, Google AI Studio, Gemini API, Django, Cloud Storage',
                problem=(
                    'Organisations held large volumes of unstructured documents and images that were impossible '
                    'to search or extract insights from at scale. Traditional keyword search and manual review '
                    'were too slow and missed critical information.'
                ),
                key_features=(
                    'PDF upload with automatic structured summarisation\n'
                    'Natural language document querying\n'
                    'Key entity and data extraction\n'
                    'Image captioning and scene analysis\n'
                    'Multi-modal chat (text + image input)\n'
                    'Cloud Storage integration for file management'
                ),
                role=(
                    'AI developer and full-stack engineer — integrated the Gemini API, designed the document '
                    'processing pipeline, built the Django backend, and delivered the frontend interface.'
                ),
                solution=(
                    'Used Gemini\'s multi-modal capabilities to build a document intelligence pipeline: '
                    'upload a PDF, auto-generate a structured summary, extract key entities, and enable '
                    'natural language querying. Extended to images with scene analysis and captioning.'
                ),
                challenge=(
                    'Handling large PDFs efficiently within Gemini\'s token limits. '
                    'Solved by chunking documents and using a map-reduce summarisation strategy.'
                ),
                learnings=(
                    'Multi-modal AI design, document chunking strategies, Gemini API capabilities and limits, '
                    'and how to build production-grade AI pipelines with Google Cloud.'
                ),
                outcome=(
                    'Reduced document review time by 80%. Users could instantly find answers across hundreds '
                    'of documents using natural language. Image analysis achieved 94% accuracy on the test set.'
                ),
                order=4, is_featured=True,
            ),
            dict(
                title='Machine Learning Project',
                short_description='Predictive analytics models built with scikit-learn to drive data-driven business decisions.',
                description=(
                    'Developed a machine learning pipeline using scikit-learn to build, evaluate, and compare '
                    'predictive models on real-world business datasets. Covers the full ML lifecycle: data '
                    'cleaning, feature engineering, model training, evaluation, and insight visualisation.'
                ),
                tools='Python, scikit-learn, pandas, NumPy, Matplotlib, Seaborn, Jupyter Notebook',
                problem=(
                    'A business was making expensive operational decisions based on intuition rather than data. '
                    'They needed predictive models to forecast demand, identify churn risk, and flag anomalies '
                    'before they became costly problems.'
                ),
                key_features=(
                    'End-to-end data preprocessing pipeline\n'
                    'Multiple model comparison (Random Forest, SVM, Logistic Regression, XGBoost)\n'
                    'Feature importance analysis and selection\n'
                    'Cross-validation and hyperparameter tuning\n'
                    'Confusion matrix and ROC curve visualisation\n'
                    'Jupyter Notebook with full reproducible workflow'
                ),
                role=(
                    'ML engineer — handled the entire pipeline independently, from raw data ingestion and '
                    'cleaning through feature engineering, model selection, tuning, and final reporting.'
                ),
                solution=(
                    'Built a reusable scikit-learn pipeline with custom transformers for preprocessing. '
                    'Trained and benchmarked multiple classifiers using cross-validation. Used GridSearchCV '
                    'for hyperparameter tuning and SHAP values for model explainability.'
                ),
                challenge=(
                    'Dealing with heavily imbalanced class distributions and noisy real-world data. '
                    'Applied SMOTE oversampling and robust scaling to address both issues without data leakage.'
                ),
                learnings=(
                    'Practical feature engineering, the impact of class imbalance on model metrics, '
                    'hyperparameter tuning strategies, and how to communicate ML results to non-technical stakeholders.'
                ),
                outcome=(
                    'Achieved 85%+ model accuracy. The churn prediction model identified at-risk customers '
                    '3 weeks in advance, enabling proactive retention campaigns that reduced churn by 22%.'
                ),
                order=5, is_featured=True,
            ),
            dict(
                title='Campus SkillSwap',
                short_description='A Django peer-to-peer skill exchange platform connecting university students to share knowledge.',
                description=(
                    'Designed and built a full-stack Django web application enabling university students to list '
                    'skills they can teach and skills they want to learn, then match with peers for structured '
                    'skill-swap sessions. Includes profiles, messaging, booking, and a rating system.'
                ),
                tools='Python, Django, SQLite, HTML, CSS, JavaScript, Bootstrap',
                problem=(
                    'University students had valuable skills to share — coding, languages, music, design — '
                    'but had no structured platform to connect with peers who needed exactly those skills. '
                    'Existing platforms were either paid or not campus-focused.'
                ),
                key_features=(
                    'Skill listing and browsing by category\n'
                    'User profiles with offered and wanted skills\n'
                    'Skill-swap request and matching system\n'
                    'In-app messaging between matched users\n'
                    'Session booking with calendar integration\n'
                    'Post-session rating and review system\n'
                    'Admin moderation panel'
                ),
                role=(
                    'Sole developer — designed the database schema, built all Django models, views, forms, '
                    'and templates, implemented the matching logic, and launched the platform for pilot testing.'
                ),
                solution=(
                    'Built a Django platform with custom user profiles extending Django\'s auth system. '
                    'Created a matching algorithm based on complementary skill sets. Added a lightweight '
                    'messaging system, booking calendar, and post-session feedback loop.'
                ),
                challenge=(
                    'Designing a fair and intuitive matching algorithm that surfaced relevant skill partners '
                    'without overwhelming users. Iterated through three approaches before settling on a '
                    'tag-based similarity score combined with activity recency.'
                ),
                learnings=(
                    'Django ORM complex relationships, custom user authentication, algorithm design for '
                    'matching systems, full-stack project planning from schema to deployment, and user '
                    'research-driven iteration.'
                ),
                outcome=(
                    'Launched to 50+ students in the campus pilot. Achieved a 90% user satisfaction rating. '
                    'Students completed 120+ skill-swap sessions in the first month of operation.'
                ),
                order=6, is_featured=True,
            ),
        ]

        updated = 0
        created = 0
        rename_map = {
            'AI Chatbot Platform': 'Chatbot Project',
            'n8n Agent Workflow Automation': 'n8n Agent Workflow Project',
            'LangChain Autonomous Agent': 'LangChain Agent Project',
            'Google AI Studio Integration': 'Google AI Studio Media Project',
        }
        for old, new in rename_map.items():
            Project.objects.filter(title=old).update(title=new)

        for p in projects:
            obj, was_created = Project.objects.get_or_create(
                title=p['title'], defaults=p,
            )
            if was_created:
                created += 1
            else:
                for k, v in p.items():
                    setattr(obj, k, v)
                obj.save()
                updated += 1
        self.stdout.write(f'  OK {created} projects created, {updated} updated.')

    # ------------------------------------------------------------------ #
    def _seed_skills(self):
        skills = [
            # Languages
            ('Python', 'languages', 5, 1),
            ('JavaScript', 'languages', 4, 2),
            ('HTML & CSS', 'languages', 5, 3),
            ('SQL', 'languages', 4, 4),
            ('TypeScript', 'languages', 3, 5),
            ('Bash / Shell', 'languages', 3, 6),
            # Frameworks
            ('Django', 'frameworks', 5, 1),
            ('FastAPI', 'frameworks', 4, 2),
            ('React', 'frameworks', 3, 3),
            ('LangChain', 'frameworks', 5, 4),
            ('Node.js', 'frameworks', 3, 5),
            # AI & ML
            ('OpenAI API', 'ai_ml', 5, 1),
            ('Google Gemini / AI Studio', 'ai_ml', 4, 2),
            ('LangChain Agents', 'ai_ml', 5, 3),
            ('Vector Databases (ChromaDB/FAISS)', 'ai_ml', 4, 4),
            ('Machine Learning (Scikit-learn)', 'ai_ml', 3, 5),
            ('Prompt Engineering', 'ai_ml', 5, 6),
            # Tools
            ('Git & GitHub', 'tools', 5, 1),
            ('Docker', 'tools', 4, 2),
            ('n8n', 'tools', 5, 3),
            ('VS Code', 'tools', 5, 4),
            ('Postman / REST APIs', 'tools', 5, 5),
            ('Linux / Unix', 'tools', 4, 6),
            # Databases
            ('SQLite', 'databases', 5, 1),
            ('PostgreSQL', 'databases', 4, 2),
            ('Redis', 'databases', 3, 3),
            ('ChromaDB', 'databases', 4, 4),
            # Soft Skills
            ('Problem Solving', 'soft_skills', 5, 1),
            ('Technical Writing', 'soft_skills', 4, 2),
            ('Communication', 'soft_skills', 5, 3),
            ('Agile / Scrum', 'soft_skills', 4, 4),
        ]
        created = 0
        for name, cat, prof, order in skills:
            _, was_created = Skill.objects.get_or_create(
                name=name, category=cat,
                defaults={'proficiency': prof, 'order': order},
            )
            if was_created:
                created += 1
        self.stdout.write(f'  OK {created} skills created.')

    # ------------------------------------------------------------------ #
    def _seed_resume(self):
        entries = [
            # Education
            dict(type='education', title='Bachelor of Science in Computer Science',
                 organization='Your University', location='City, Country',
                 start_date='Sep 2019', end_date='Jun 2023',
                 description='Graduated with First Class Honours. Specialised in AI and software engineering.',
                 bullet_points='Dissertation: "Autonomous Agents Using Reinforcement Learning"\nDean\'s List all four years\nPresented research at two national conferences',
                 order=1),
            dict(type='education', title='Advanced Python & AI Certificate',
                 organization='Online Learning Platform', location='Remote',
                 start_date='Jan 2024', end_date='Mar 2024',
                 description='Completed advanced coursework in Python, machine learning, and AI application development.',
                 order=2),
            # Experience
            dict(type='experience', title='Full-Stack Developer (Freelance)',
                 organization='Self-Employed', location='Remote',
                 start_date='Jan 2024', end_date='',
                 description='Building AI-powered web applications and automation workflows for clients across various industries.',
                 bullet_points='Delivered 8+ client projects on time and within budget\nBuilt a LangChain-powered document assistant for a law firm\nDesigned n8n automation workflows saving clients 20+ hours/week\nMaintained 5-star client satisfaction rating across all engagements',
                 order=1),
            dict(type='experience', title='Junior Python Developer',
                 organization='Tech Company', location='City, Country',
                 start_date='Jul 2023', end_date='Dec 2023',
                 description='Developed and maintained Python microservices and Django REST APIs for a SaaS product with 10,000+ users.',
                 bullet_points='Reduced API response times by 40% through query optimisation\nBuilt automated testing pipeline reducing bug detection time by 60%\nOnboarded and mentored two junior developers',
                 order=2),
            # Certifications
            dict(type='certification', title='Google AI Essentials',
                 organization='Google', start_date='2024', order=1),
            dict(type='certification', title='AWS Cloud Practitioner',
                 organization='Amazon Web Services', start_date='2023', order=2),
            dict(type='certification', title='Python for Everybody',
                 organization='Coursera / University of Michigan', start_date='2022', order=3),
            # Achievements
            dict(type='achievement', title='1st Place — University Hackathon',
                 organization='University of Technology',
                 description='Built an AI-powered accessibility tool that won first place out of 60 teams.',
                 order=1),
            dict(type='achievement', title='Open Source Contributor',
                 organization='GitHub',
                 description='Contributor to several open-source Python and AI libraries with 200+ GitHub stars.',
                 order=2),
        ]
        created = 0
        for e in entries:
            e_copy = {k: v for k, v in e.items()}
            _, was_created = ResumeSection.objects.get_or_create(
                type=e_copy.pop('type'),
                title=e_copy.pop('title'),
                defaults=e_copy,
            )
            if was_created:
                created += 1
        self.stdout.write(f'  OK {created} resume entries created.')
