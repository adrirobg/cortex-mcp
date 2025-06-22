"""Domain Intelligence Heuristics module for CortexMCP Phase 2.8.2.

Implements multi-dimensional domain analysis with confidence scoring for collaborative 
domain selection. Replaces primitive keyword matching with sophisticated heuristics
that consider context, complexity, and technology patterns.

Following Principios Rectores:
1. Dogmatismo con Universal Response Schema - strict schema validation
2. Servidor como Ejecutor Fiable - deterministic heuristics, no AI magic
3. Estado en Claude, NO en Servidor - pure functions, no state
4. Testing Concurrente - comprehensive test coverage
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from schemas.architect_payloads import DomainAnalysisContext, DomainOption


# Enhanced domain classification with multi-dimensional analysis
DOMAIN_KEYWORDS = {
    'web_app': {
        'primary': ['web', 'website', 'frontend', 'backend', 'fullstack', 'webapp'],
        'technologies': ['html', 'css', 'javascript', 'react', 'vue', 'angular', 'django', 'flask', 'fastapi', 'express', 'nextjs', 'nuxt'],
        'patterns': ['spa', 'ssr', 'pwa', 'responsive', 'ui/ux', 'dashboard', 'admin panel'],
        'contexts': ['e-commerce', 'platform', 'portal', 'application']
    },
    'cli_tooling': {
        'primary': ['cli', 'command line', 'terminal', 'script', 'automation', 'tool'],
        'technologies': ['bash', 'shell', 'python', 'node', 'go', 'rust'],
        'patterns': ['slash command', 'mcp', 'integration', 'workflow', 'utility'],
        'contexts': ['claude code', 'vscode', 'ide', 'developer tools', 'productivity']
    },
    'system_architecture': {
        'primary': ['architecture', 'system', 'infrastructure', 'platform', 'framework'],
        'technologies': ['mcp', 'server', 'protocol', 'microservices', 'distributed'],
        'patterns': ['refactor', 'redesign', 'migration', 'modernization', 'scalability'],
        'contexts': ['enterprise', 'production', 'high-performance', 'reliability']
    },
    'data_science': {
        'primary': ['data', 'analytics', 'ml', 'ai', 'machine learning', 'model'],
        'technologies': ['python', 'pandas', 'numpy', 'tensorflow', 'pytorch', 'scikit-learn'],
        'patterns': ['pipeline', 'etl', 'analysis', 'prediction', 'classification'],
        'contexts': ['insights', 'intelligence', 'automation', 'decision making']
    },
    'api_service': {
        'primary': ['api', 'service', 'endpoint', 'microservice', 'rest', 'graphql'],
        'technologies': ['fastapi', 'express', 'spring', 'django rest', 'flask'],
        'patterns': ['crud', 'authentication', 'authorization', 'integration'],
        'contexts': ['backend', 'server-side', 'business logic', 'data access']
    },
    'mobile_app': {
        'primary': ['mobile', 'app', 'android', 'ios', 'smartphone', 'tablet'],
        'technologies': ['react-native', 'flutter', 'swift', 'kotlin', 'xamarin'],
        'patterns': ['responsive', 'touch', 'native', 'cross-platform'],
        'contexts': ['user experience', 'performance', 'app store', 'device']
    },
    'devops_infrastructure': {
        'primary': ['devops', 'infrastructure', 'deployment', 'ci/cd', 'ops'],
        'technologies': ['docker', 'kubernetes', 'terraform', 'ansible', 'jenkins'],
        'patterns': ['automation', 'monitoring', 'scalability', 'reliability'],
        'contexts': ['aws', 'azure', 'gcp', 'cloud', 'production']
    },
    'general_software': {
        'primary': ['software', 'application', 'system', 'tool', 'solution'],
        'technologies': ['programming', 'development', 'coding'],
        'patterns': ['build', 'create', 'develop', 'implement'],
        'contexts': ['project', 'feature', 'functionality', 'requirements']
    }
}

# Technology stack patterns with weights
TECHNOLOGY_PATTERNS = {
    'python + fastapi + pydantic': ('api_service', 0.9),
    'python + mcp + server': ('system_architecture', 0.85),
    'javascript + react + node': ('web_app', 0.8),
    'bash + cli + terminal': ('cli_tooling', 0.9),
    'python + pandas + ml': ('data_science', 0.85),
    'docker + kubernetes + cloud': ('devops_infrastructure', 0.8),
    'mobile + react-native + app': ('mobile_app', 0.9),
    'api + rest + microservice': ('api_service', 0.8)
}

# Complexity indicators affecting confidence
COMPLEXITY_INDICATORS = {
    'high': ['enterprise', 'scalable', 'distributed', 'microservices', 'production', 'high-performance'],
    'medium': ['integration', 'authentication', 'database', 'api', 'frontend', 'backend'],
    'low': ['simple', 'basic', 'prototype', 'demo', 'example', 'tutorial']
}

# Context patterns for better classification
CONTEXT_PATTERNS = {
    'existing_codebase': r'\b(refactor|modify|enhance|improve|update|migrate|modernize)\b',
    'new_project': r'\b(create|build|develop|implement|design|start)\b',
    'integration': r'\b(integrate|connect|link|sync|mcp|protocol)\b',
    'user_interface': r'\b(ui|ux|interface|frontend|dashboard|admin)\b',
    'data_processing': r'\b(data|analytics|processing|pipeline|etl)\b',
    'automation': r'\b(automate|script|tool|cli|command)\b'
}


@dataclass
class DomainIndicators:
    """Structured domain analysis indicators."""
    keyword_matches: Dict[str, List[str]]
    technology_patterns: List[Tuple[str, float]]
    complexity_level: str
    context_matches: List[str]
    description_length: int


def analyze_keywords(task_description: str) -> Dict[str, List[str]]:
    """Analyze keywords across all domains with weighted scoring.
    
    Args:
        task_description: Project description text
        
    Returns:
        Dictionary mapping domain to matched keywords
    """
    description_lower = task_description.lower()
    domain_matches = {}
    
    for domain, categories in DOMAIN_KEYWORDS.items():
        matches = []
        
        # Check all keyword categories
        for category, keywords in categories.items():
            for keyword in keywords:
                keyword_lower = keyword.lower()
                # Handle different variations
                variations = [
                    keyword_lower,
                    keyword_lower.replace('-', ' '),
                    keyword_lower.replace(' ', '-'),
                    keyword_lower.replace(' ', ''),
                ]
                
                for variation in variations:
                    if variation in description_lower:
                        matches.append(f"{keyword} ({category})")
                        break
        
        if matches:
            domain_matches[domain] = matches
    
    return domain_matches


def detect_technology_patterns(task_description: str) -> List[Tuple[str, float]]:
    """Detect technology stack combinations with confidence scores.
    
    Args:
        task_description: Project description text
        
    Returns:
        List of (pattern, confidence) tuples
    """
    description_lower = task_description.lower()
    detected_patterns = []
    
    # Enhanced pattern detection with synonyms and variations
    enhanced_patterns = {
        'python + fastapi + pydantic': ('api_service', 0.9),
        'python + mcp + server': ('system_architecture', 0.85),
        'javascript + react + node': ('web_app', 0.8),
        'bash + cli + terminal': ('cli_tooling', 0.9),
        'python + pandas + ml': ('data_science', 0.85),
        'docker + kubernetes + cloud': ('devops_infrastructure', 0.8),
        'mobile + react-native + app': ('mobile_app', 0.9),
        'api + rest + microservice': ('api_service', 0.8),
        'fastapi + react': ('web_app', 0.85),  # Common combo
        'react + frontend': ('web_app', 0.8),
        'fastapi + backend': ('api_service', 0.8),
        'react + backend': ('web_app', 0.75),
        'frontend + backend': ('web_app', 0.7),
        'e-commerce + platform': ('web_app', 0.75)
    }
    
    for pattern, (domain, base_confidence) in enhanced_patterns.items():
        pattern_words = pattern.lower().split(' + ')
        matches = sum(1 for word in pattern_words if word in description_lower)
        
        if matches >= 2:  # Require at least 2 components
            pattern_confidence = base_confidence * (matches / len(pattern_words))
            detected_patterns.append((f"{pattern} → {domain}", pattern_confidence))
        elif matches == 1 and len(pattern_words) == 2:  # For 2-word patterns, 1 match is still valuable
            pattern_confidence = base_confidence * 0.5
            detected_patterns.append((f"{pattern} → {domain}", pattern_confidence))
    
    return sorted(detected_patterns, key=lambda x: x[1], reverse=True)


def assess_complexity(task_description: str) -> str:
    """Assess project complexity based on indicators.
    
    Args:
        task_description: Project description text
        
    Returns:
        Complexity level: "low", "medium", or "high"
    """
    description_lower = task_description.lower()
    complexity_scores = {'high': 0, 'medium': 0, 'low': 0}
    
    for level, indicators in COMPLEXITY_INDICATORS.items():
        for indicator in indicators:
            if indicator in description_lower:
                complexity_scores[level] += 1
    
    # Add length-based complexity
    length = len(task_description)
    if length > 200:
        complexity_scores['high'] += 2
    elif length > 100:
        complexity_scores['medium'] += 1
    else:
        complexity_scores['low'] += 1
    
    return max(complexity_scores.keys(), key=lambda x: complexity_scores[x])


def detect_context_patterns(task_description: str) -> List[str]:
    """Detect contextual patterns that influence domain classification.
    
    Args:
        task_description: Project description text
        
    Returns:
        List of detected context patterns
    """
    description_lower = task_description.lower()
    detected_contexts = []
    
    for context_name, pattern_regex in CONTEXT_PATTERNS.items():
        if re.search(pattern_regex, description_lower, re.IGNORECASE):
            detected_contexts.append(context_name)
    
    return detected_contexts


def calculate_confidence_scores(indicators: DomainIndicators) -> Dict[str, float]:
    """Calculate confidence scores for each domain based on multi-dimensional analysis.
    
    Args:
        indicators: Analyzed domain indicators
        
    Returns:
        Dictionary mapping domain to confidence score (0.0-1.0)
    """
    confidence_scores = {}
    
    for domain in DOMAIN_KEYWORDS.keys():
        score = 0.0
        
        # Keyword matching score (50% weight) - increased importance
        keyword_matches = indicators.keyword_matches.get(domain, [])
        if keyword_matches:
            # Enhanced scoring based on keyword category and count
            primary_keywords = sum(1 for kw in keyword_matches if '(primary)' in kw)
            tech_keywords = sum(1 for kw in keyword_matches if '(technologies)' in kw)
            pattern_keywords = sum(1 for kw in keyword_matches if '(patterns)' in kw)
            context_keywords = sum(1 for kw in keyword_matches if '(contexts)' in kw)
            
            # Weighted keyword scoring
            keyword_score = (
                primary_keywords * 0.4 +
                tech_keywords * 0.3 +
                pattern_keywords * 0.2 +
                context_keywords * 0.1
            )
            keyword_score = min(keyword_score, 1.0)
            score += keyword_score * 0.5
        
        # Technology pattern score (35% weight) - increased importance
        tech_score = 0.0
        for pattern, pattern_confidence in indicators.technology_patterns:
            if domain in pattern:
                tech_score = max(tech_score, pattern_confidence)
        score += tech_score * 0.35
        
        # Context pattern score (10% weight) - reduced weight
        context_score = 0.0
        domain_context_map = {
            'web_app': ['user_interface', 'new_project'],
            'cli_tooling': ['automation', 'integration'],
            'system_architecture': ['existing_codebase', 'integration'],
            'data_science': ['data_processing'],
            'api_service': ['integration'],
            'mobile_app': ['user_interface', 'new_project'],
            'devops_infrastructure': ['automation', 'existing_codebase'],
            'general_software': ['new_project']
        }
        
        if domain in domain_context_map:
            relevant_contexts = domain_context_map[domain]
            context_matches = sum(1 for ctx in relevant_contexts if ctx in indicators.context_matches)
            context_score = min(context_matches * 0.6, 1.0)
        score += context_score * 0.1
        
        # Complexity adjustment (5% weight) - reduced weight
        complexity_bonus = {
            'system_architecture': {'medium': 0.2, 'high': 0.4},
            'data_science': {'medium': 0.2, 'high': 0.4},
            'devops_infrastructure': {'medium': 0.2, 'high': 0.4},
            'web_app': {'low': 0.1, 'medium': 0.2},
            'cli_tooling': {'low': 0.1, 'medium': 0.2}
        }
        
        if domain in complexity_bonus and indicators.complexity_level in complexity_bonus[domain]:
            score += complexity_bonus[domain][indicators.complexity_level] * 0.05
        
        confidence_scores[domain] = min(score, 1.0)
    
    # Apply bonus for strong technology stack matches
    for domain in confidence_scores:
        tech_boost = 0
        if domain == 'web_app' and any('fastapi' in pattern.lower() and 'react' in pattern.lower() for pattern, _ in indicators.technology_patterns):
            tech_boost = 0.3
        elif domain == 'api_service' and any('fastapi' in pattern.lower() for pattern, _ in indicators.technology_patterns):
            tech_boost = 0.25
        elif domain == 'data_science' and any('pandas' in pattern.lower() or 'ml' in pattern.lower() for pattern, _ in indicators.technology_patterns):
            tech_boost = 0.25
        
        confidence_scores[domain] = min(confidence_scores[domain] + tech_boost, 1.0)
    
    return confidence_scores


def generate_domain_options(scores: Dict[str, float], threshold: float = 0.3) -> List[DomainOption]:
    """Generate domain options above confidence threshold.
    
    Args:
        scores: Domain confidence scores
        threshold: Minimum confidence threshold
        
    Returns:
        List of DomainOption objects sorted by confidence
    """
    options = []
    
    for domain, confidence in scores.items():
        if confidence >= threshold:
            # Generate supporting evidence
            evidence = []
            if confidence > 0.7:
                evidence.append(f"High keyword relevance for {domain.replace('_', ' ')}")
            if confidence > 0.5:
                evidence.append("Technology stack alignment detected")
            if confidence > 0.4:
                evidence.append("Context patterns match domain characteristics")
            
            # Generate potential concerns
            concerns = []
            if confidence < 0.6:
                concerns.append("Moderate confidence - may need clarification")
            if domain == 'general_software':
                concerns.append("Generic classification - consider more specific domain")
            
            option = DomainOption(
                domain_id=domain,
                domain_name=domain.replace('_', ' ').title(),
                confidence_score=confidence,
                supporting_evidence=evidence,
                potential_concerns=concerns
            )
            options.append(option)
    
    return sorted(options, key=lambda x: x.confidence_score, reverse=True)


def analyze_domain_indicators(task_description: str) -> 'DomainAnalysisResult':
    """Perform comprehensive multi-dimensional domain analysis.
    
    Main function implementing sophisticated domain detection with confidence scoring.
    
    Args:
        task_description: Project description to analyze
        
    Returns:
        DomainAnalysisResult with complete analysis context
        
    Raises:
        ValueError: If task_description is empty or invalid
    """
    if not task_description or not task_description.strip():
        raise ValueError("task_description cannot be empty")
    
    # Multi-dimensional analysis
    keyword_matches = analyze_keywords(task_description)
    technology_patterns = detect_technology_patterns(task_description)
    complexity_level = assess_complexity(task_description)
    context_matches = detect_context_patterns(task_description)
    
    # Create indicators structure
    indicators = DomainIndicators(
        keyword_matches=keyword_matches,
        technology_patterns=technology_patterns,
        complexity_level=complexity_level,
        context_matches=context_matches,
        description_length=len(task_description)
    )
    
    # Calculate confidence scores
    confidence_scores = calculate_confidence_scores(indicators)
    
    # Generate domain options
    domain_options = generate_domain_options(confidence_scores)
    
    # Determine recommended domain
    recommended_domain = domain_options[0].domain_id if domain_options else 'general_software'
    max_confidence = domain_options[0].confidence_score if domain_options else 0.1
    
    # Create analysis context
    analysis_context = DomainAnalysisContext(
        detected_keywords={domain: [kw.split(' (')[0] for kw in keywords] 
                          for domain, keywords in keyword_matches.items()},
        technology_indicators=[pattern.split(' → ')[0] for pattern, _ in technology_patterns],
        complexity_assessment=complexity_level,
        confidence_breakdown=confidence_scores
    )
    
    return DomainAnalysisResult(
        domain_options=domain_options,
        recommended_domain=recommended_domain,
        max_confidence=max_confidence,
        analysis_context=analysis_context,
        requires_collaboration=max_confidence < 0.7,
        confidence_scores=confidence_scores
    )


@dataclass
class DomainAnalysisResult:
    """Complete domain analysis result with collaboration indicators."""
    domain_options: List[DomainOption]
    recommended_domain: str
    max_confidence: float
    analysis_context: DomainAnalysisContext
    requires_collaboration: bool
    confidence_scores: Dict[str, float]