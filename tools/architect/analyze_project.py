"""Analyze Project module for Strategy Library MCP Server.

Implements deterministic heuristics for project analysis following Phase 2.1 specifications.
Returns AnalysisResult with extracted keywords, patterns, and complexity assessment.

Following Principios Rectores:
1. Dogmatismo con Universal Response Schema - strict AnalysisResult validation
2. Servidor como Ejecutor Fiable - deterministic heuristics, no AI magic
3. Estado en Claude, NO en Servidor - pure functions, no state
4. Testing Concurrente - comprehensive test coverage
"""

import re
from typing import List, Optional
from schemas.architect_payloads import AnalysisResult


# Domain keywords mapping for project classification
DOMAIN_KEYWORDS = {
    'web': ['web', 'website', 'frontend', 'backend', 'html', 'css', 'javascript', 'react', 'vue', 'angular', 'django', 'flask', 'express', 'nextjs', 'nuxt'],
    'api': ['api', 'rest', 'graphql', 'endpoint', 'service', 'microservice', 'webhook', 'integration', 'oauth', 'authentication', 'authorization'],
    'data': ['data', 'database', 'analytics', 'pipeline', 'etl', 'warehouse', 'sql', 'mongodb', 'postgresql', 'mysql', 'redis', 'elasticsearch'],
    'mobile': ['mobile', 'app', 'android', 'ios', 'react-native', 'flutter', 'xamarin', 'cordova', 'phonegap', 'ionic'],
    'ai': ['ai', 'ml', 'machine learning', 'neural', 'model', 'prediction', 'tensorflow', 'pytorch', 'scikit-learn', 'nlp', 'computer vision'],
    'devops': ['docker', 'kubernetes', 'ci/cd', 'deployment', 'infrastructure', 'aws', 'azure', 'gcp', 'terraform', 'ansible'],
    'security': ['security', 'encryption', 'ssl', 'tls', 'authentication', 'authorization', 'vulnerability', 'penetration', 'audit'],
    'ecommerce': ['ecommerce', 'payment', 'stripe', 'paypal', 'cart', 'checkout', 'inventory', 'order', 'product catalog'],
    'social': ['social', 'chat', 'messaging', 'notification', 'feed', 'timeline', 'user profiles', 'friends', 'followers'],
    'gaming': ['game', 'gaming', 'unity', 'unreal', 'multiplayer', 'leaderboard', 'achievements', 'physics engine']
}

# Common project patterns for pattern detection
PROJECT_PATTERNS = {
    'crud_operations': r'\b(create|read|update|delete|crud)\b',
    'user_management': r'\b(user|login|register|profile|authentication|signup|signin)\b',
    'real_time': r'\b(real.?time|websocket|live|streaming|chat|notification)\b',
    'file_handling': r'\b(file|upload|download|storage|document|image|video)\b',
    'integration': r'\b(api|integration|third.?party|external|webhook|sync)\b',
    'dashboard': r'\b(dashboard|admin|analytics|reporting|metrics|charts)\b',
    'search': r'\b(search|filter|query|elasticsearch|solr|indexing)\b',
    'payment': r'\b(payment|billing|subscription|transaction|checkout|stripe|paypal)\b',
    'workflow': r'\b(workflow|process|automation|pipeline|approval|review)\b',
    'multi_tenant': r'\b(multi.?tenant|tenant|organization|workspace|team)\b'
}

# Technology stack indicators
TECH_STACK_INDICATORS = {
    'python': ['python', 'django', 'flask', 'fastapi', 'pandas', 'numpy'],
    'javascript': ['javascript', 'js', 'node', 'react', 'vue', 'angular', 'express'],
    'java': ['java', 'spring', 'hibernate', 'maven', 'gradle'],
    'dotnet': ['.net', 'c#', 'asp.net', 'entity framework'],
    'php': ['php', 'laravel', 'symfony', 'wordpress', 'drupal'],
    'ruby': ['ruby', 'rails', 'gem', 'bundler'],
    'go': ['go', 'golang', 'gin', 'echo'],
    'rust': ['rust', 'cargo', 'actix', 'rocket']
}


def extract_keywords(task_description: str) -> List[str]:
    """Extract domain-specific keywords from task description.
    
    Uses DOMAIN_KEYWORDS mapping to identify relevant project domains.
    Handles multi-word keywords and hyphenated terms.
    
    Args:
        task_description: Project description text
        
    Returns:
        List of unique keywords found in the description
    """
    description_lower = task_description.lower()
    found_keywords = []
    
    for domain, keywords in DOMAIN_KEYWORDS.items():
        for keyword in keywords:
            keyword_lower = keyword.lower()
            # Handle different variations of the keyword
            variations = [
                keyword_lower,
                keyword_lower.replace('-', ' '),  # react-native -> react native
                keyword_lower.replace(' ', '-'),  # react native -> react-native
                keyword_lower.replace(' ', ''),   # react native -> reactnative
            ]
            
            for variation in variations:
                if variation in description_lower:
                    found_keywords.append(keyword)
                    break  # Found this keyword, move to next
    
    # Remove duplicates and return sorted
    return sorted(list(set(found_keywords)))


def detect_patterns(task_description: str) -> List[str]:
    """Detect common project patterns using regex matching.
    
    Uses PROJECT_PATTERNS mapping to identify architectural patterns.
    
    Args:
        task_description: Project description text
        
    Returns:
        List of detected pattern names
    """
    description_lower = task_description.lower()
    detected_patterns = []
    
    for pattern_name, pattern_regex in PROJECT_PATTERNS.items():
        if re.search(pattern_regex, description_lower, re.IGNORECASE):
            detected_patterns.append(pattern_name)
    
    return sorted(detected_patterns)


def calculate_complexity(task_description: str, keywords: List[str]) -> str:
    """Calculate project complexity using deterministic heuristics.
    
    Based on description length, keyword count, and pattern complexity.
    
    Args:
        task_description: Project description text
        keywords: Extracted keywords list
        
    Returns:
        Complexity level: "Baja", "Media", or "Alta"
    """
    description_len = len(task_description)
    keyword_count = len(keywords)
    
    # Base complexity on description length
    if description_len < 50:
        base_complexity = 1
    elif description_len < 150:
        base_complexity = 2
    else:
        base_complexity = 3
    
    # Adjust based on keyword diversity
    if keyword_count > 12:
        base_complexity += 2
    elif keyword_count > 6:
        base_complexity += 1
    
    # Map to complexity levels
    if base_complexity <= 2:
        return "Baja"
    elif base_complexity <= 4:
        return "Media"
    else:
        return "Alta"


def classify_domain(keywords: List[str]) -> Optional[str]:
    """Classify project domain based on keyword density.
    
    Determines primary domain based on which domain has most matching keywords.
    Web domain gets priority when tied with API domain.
    
    Args:
        keywords: List of extracted keywords
        
    Returns:
        Primary domain name or None if no clear domain
    """
    if not keywords:
        return None
    
    domain_scores = {}
    keywords_lower = [k.lower() for k in keywords]
    
    for domain, domain_keywords in DOMAIN_KEYWORDS.items():
        score = sum(1 for kw in domain_keywords if kw.lower() in keywords_lower)
        if score > 0:
            domain_scores[domain] = score
    
    if not domain_scores:
        return None
    
    # Get max score
    max_score = max(domain_scores.values())
    
    # If web and api have same score, prioritize web
    if domain_scores.get('web', 0) == max_score and domain_scores.get('api', 0) == max_score:
        return 'web'
    
    # Return domain with highest score
    return max(domain_scores.keys(), key=lambda x: domain_scores[x])


def suggest_technology_stack(keywords: List[str], domain: Optional[str]) -> List[str]:
    """Suggest technology stack based on keywords and domain.
    
    Uses TECH_STACK_INDICATORS and domain context to suggest technologies.
    
    Args:
        keywords: Extracted keywords
        domain: Classified domain
        
    Returns:
        List of suggested technologies
    """
    tech_suggestions = []
    keywords_lower = [k.lower() for k in keywords]
    
    # Direct technology matches
    for tech, indicators in TECH_STACK_INDICATORS.items():
        if any(indicator.lower() in keywords_lower for indicator in indicators):
            tech_suggestions.append(tech)
    
    # Domain-based suggestions (if no direct matches)
    if not tech_suggestions and domain:
        domain_tech_map = {
            'web': ['javascript', 'python'],
            'api': ['python', 'javascript', 'java'],
            'data': ['python', 'java'],
            'mobile': ['javascript', 'java'],
            'ai': ['python'],
            'devops': ['python', 'go'],
            'ecommerce': ['javascript', 'python', 'php'],
            'gaming': ['javascript', 'python']
        }
        tech_suggestions = domain_tech_map.get(domain, [])
    
    return tech_suggestions


def extract_implicit_requirements(task_description: str, patterns: List[str], domain: Optional[str]) -> List[str]:
    """Extract implicit requirements based on patterns and domain.
    
    Infers common requirements based on detected patterns and domain.
    
    Args:
        task_description: Project description
        patterns: Detected patterns
        domain: Classified domain
        
    Returns:
        List of implicit requirements
    """
    requirements = []
    
    # Pattern-based requirements
    pattern_requirements = {
        'crud_operations': 'Database design and ORM integration',
        'user_management': 'Authentication and authorization system',
        'real_time': 'WebSocket or Server-Sent Events implementation',
        'file_handling': 'File storage and processing system',
        'integration': 'API design and third-party service integration',
        'dashboard': 'Data visualization and reporting capabilities',
        'search': 'Search indexing and query optimization',
        'payment': 'Payment gateway integration and security compliance',
        'workflow': 'State management and process automation',
        'multi_tenant': 'Data isolation and tenant management'
    }
    
    for pattern in patterns:
        if pattern in pattern_requirements:
            requirements.append(pattern_requirements[pattern])
    
    # Domain-based requirements
    domain_requirements = {
        'web': 'Responsive design and cross-browser compatibility',
        'api': 'API documentation and versioning strategy',
        'data': 'Data validation and backup strategies',
        'mobile': 'Platform-specific optimization and app store compliance',
        'ai': 'Model training pipeline and data preprocessing',
        'devops': 'Infrastructure as code and monitoring setup',
        'security': 'Security audit and compliance validation',
        'ecommerce': 'Inventory management and order processing',
        'social': 'Content moderation and privacy controls',
        'gaming': 'Performance optimization and user experience design'
    }
    
    if domain and domain in domain_requirements:
        requirements.append(domain_requirements[domain])
    
    # General requirements based on complexity
    if len(task_description) > 100:
        requirements.extend([
            'Comprehensive testing strategy',
            'Documentation and API specifications',
            'Error handling and logging system'
        ])
    
    return list(set(requirements))


def analyze_project(task_description: str) -> AnalysisResult:
    """Analyze project description and return structured analysis result.
    
    Main function implementing deterministic heuristics for project analysis.
    Following Phase 2.1 specifications with complete validation.
    
    Args:
        task_description: Project description to analyze
        
    Returns:
        AnalysisResult with all required fields populated
        
    Raises:
        ValueError: If task_description is empty or invalid
    """
    if not task_description or not task_description.strip():
        raise ValueError("task_description cannot be empty")
    
    # Extract keywords using domain mapping
    keywords = extract_keywords(task_description)
    
    # Detect architectural patterns
    patterns = detect_patterns(task_description)
    
    # Calculate complexity using heuristics
    complexity = calculate_complexity(task_description, keywords)
    
    # Classify primary domain
    domain = classify_domain(keywords)
    
    # Suggest technology stack
    technology_stack = suggest_technology_stack(keywords, domain)
    
    # Extract implicit requirements
    requirements_implicit = extract_implicit_requirements(task_description, patterns, domain)
    
    # Create and validate AnalysisResult
    result = AnalysisResult(
        keywords=keywords,
        patterns=patterns,
        complexity=complexity,
        requirements_implicit=requirements_implicit,
        domain=domain,
        technology_stack=technology_stack
    )
    
    return result