import fitz  # PyMuPDF
from docx import Document
import re
import os

class ResumeParser:
    def __init__(self):
        self.allowed_extensions = {'pdf', 'doc', 'docx'}
    
    def allowed_file(self, filename):
        """Check if file extension is allowed"""
        return '.' in filename and \
               filename.rsplit('.', 1)[1].lower() in self.allowed_extensions
    
    def extract_text_from_pdf(self, filepath):
        """Extract text from PDF file"""
        doc = fitz.open(filepath)
        text = ""
        for page in doc:
            text += page.get_text()
        doc.close()
        return text
    
    def extract_text_from_docx(self, filepath):
        """Extract text from DOCX file"""
        doc = Document(filepath)
        text = ""
        for paragraph in doc.paragraphs:
            text += paragraph.text + "\n"
        return text
    
    def extract_text_from_doc(self, filepath):
        """Extract text from DOC file (basic support)"""
        # For DOC files, we'll try to read as binary and extract readable text
        # This is a simplified approach - for production, consider using python-docx2txt
        try:
            with open(filepath, 'rb') as f:
                content = f.read()
                # Simple text extraction - this may not work perfectly for all DOC files
                text = content.decode('utf-8', errors='ignore')
                return text
        except:
            return "Unable to parse DOC file. Please convert to DOCX or PDF format."
    
    def extract_email(self, text):
        """Extract email addresses from text"""
        email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        emails = re.findall(email_pattern, text)
        return emails[0] if emails else None
    
    def extract_phone(self, text):
        """Extract phone numbers from text"""
        phone_patterns = [
            r'\+?1?[-.\s]?$$?([0-9]{3})$$?[-.\s]?([0-9]{3})[-.\s]?([0-9]{4})',
            r'\+?([0-9]{1,3})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})[-.\s]?([0-9]{3,4})',
            r'(\d{3}[-.\s]?\d{3}[-.\s]?\d{4})',
            r'(\+\d{1,3}\s?\d{3,4}\s?\d{3,4}\s?\d{3,4})',
            r'(\d{10,})'
        ]
        
        for pattern in phone_patterns:
            try:
                matches = re.findall(pattern, text)
                if matches:
                    if isinstance(matches[0], tuple):
                        return ''.join(matches[0])
                    return matches[0]
            except re.error:
                continue
        return None
    
    def extract_name(self, text):
        """Extract name from resume text (simplified approach)"""
        lines = text.split('\n')
        # Usually the name is in the first few lines
        for line in lines[:5]:
            line = line.strip()
            if line and len(line.split()) >= 2 and len(line) < 50:
                # Check if it looks like a name (not email, phone, etc.)
                try:
                    if not re.search(r'[@\d]', line) and not line.lower().startswith(('resume', 'cv', 'curriculum')):
                        return line
                except re.error:
                    # If regex fails, use simple checks
                    if '@' not in line and not any(char.isdigit() for char in line) and not line.lower().startswith(('resume', 'cv', 'curriculum')):
                        return line
        return "Name not found"
    
    def extract_skills(self, text):
        """Extract skills from resume text"""
        skills_keywords = [
            'skills', 'technical skills', 'core competencies', 'technologies',
            'programming languages', 'tools', 'frameworks'
        ]
        
        skills = []
        lines = text.split('\n')
        
        for i, line in enumerate(lines):
            line_lower = line.lower().strip()
            if any(keyword in line_lower for keyword in skills_keywords):
                # Look at the next few lines for skills
                for j in range(i+1, min(i+10, len(lines))):
                    skill_line = lines[j].strip()
                    if skill_line and not skill_line.lower().startswith(('experience', 'education', 'project')):
                        # Split by common delimiters with better regex handling
                        try:
                            potential_skills = re.split(r'[,;|•\n]', skill_line)
                            for skill in potential_skills:
                                skill = skill.strip()
                                if skill and len(skill) < 30 and not re.search(r'^\d+$', skill):
                                    skills.append(skill)
                        except re.error:
                            # If regex fails, split by simple delimiters
                            potential_skills = skill_line.replace(',', '|').replace(';', '|').replace('•', '|').split('|')
                            for skill in potential_skills:
                                skill = skill.strip()
                                if skill and len(skill) < 30:
                                    skills.append(skill)
                else:
                    break
            break
    
        return list(set(skills))[:10]  # Return unique skills, max 10
    
    def extract_experience(self, text):
        """Extract work experience from resume text"""
        experience = []
        lines = text.split('\n')
        
        experience_keywords = ['experience', 'work experience', 'employment', 'career']
        education_keywords = ['education', 'academic', 'degree', 'university', 'college']
        
        in_experience_section = False
        current_job = {}
        
        for line in lines:
            line = line.strip()
            line_lower = line.lower()
            
            # Check if we're entering experience section
            if any(keyword in line_lower for keyword in experience_keywords):
                in_experience_section = True
                continue
            
            # Check if we're leaving experience section
            if in_experience_section and any(keyword in line_lower for keyword in education_keywords):
                if current_job:
                    experience.append(current_job)
                break
            
            if in_experience_section and line:
                # Look for job titles and companies
                if re.search(r'\d{4}', line):  # Line contains year
                    if current_job:
                        experience.append(current_job)
                    current_job = {'title': line, 'description': ''}
                elif current_job and len(line) > 20:
                    current_job['description'] += line + ' '
        
        if current_job:
            experience.append(current_job)
        
        return experience[:3]  # Return max 3 experiences
    
    def extract_education(self, text):
        """Extract education information from resume text"""
        education = []
        lines = text.split('\n')
        
        education_keywords = ['education', 'academic', 'degree', 'university', 'college', 'school']
        
        in_education_section = False
        
        for line in lines:
            line = line.strip()
            line_lower = line.lower()
            
            if any(keyword in line_lower for keyword in education_keywords):
                in_education_section = True
                continue
            
            if in_education_section and line:
                if any(word in line_lower for word in ['bachelor', 'master', 'phd', 'degree', 'diploma']):
                    education.append(line)
                elif re.search(r'\d{4}', line) and len(education) < 3:
                    education.append(line)
        
        return education[:2]  # Return max 2 education entries
    
    def parse_resume(self, filepath):
        """Main method to parse resume and extract structured data"""
        try:
            file_extension = filepath.rsplit('.', 1)[1].lower()
            
            # Extract text based on file type
            if file_extension == 'pdf':
                text = self.extract_text_from_pdf(filepath)
            elif file_extension == 'docx':
                text = self.extract_text_from_docx(filepath)
            elif file_extension == 'doc':
                text = self.extract_text_from_doc(filepath)
            else:
                raise ValueError("Unsupported file format")
            
            if not text or len(text.strip()) < 10:
                raise ValueError("Could not extract meaningful text from the file")
            
            # Extract structured information with error handling
            parsed_data = {
                'name': self.safe_extract(self.extract_name, text, "Name not found"),
                'email': self.safe_extract(self.extract_email, text, None),
                'phone': self.safe_extract(self.extract_phone, text, None),
                'skills': self.safe_extract(self.extract_skills, text, []),
                'experience': self.safe_extract(self.extract_experience, text, []),
                'education': self.safe_extract(self.extract_education, text, []),
                'bio': text[:500] + "..." if len(text) > 500 else text,
                'raw_text': text[:1000] + "..." if len(text) > 1000 else text  # Limit raw text size
            }
            
            return parsed_data
            
        except Exception as e:
            raise Exception(f"Error parsing resume: {str(e)}")

    def safe_extract(self, extract_func, text, default_value):
        """Safely execute extraction functions with error handling"""
        try:
            return extract_func(text)
        except Exception as e:
            print(f"Warning: {extract_func.__name__} failed: {str(e)}")
            return default_value
