from prompt_versioner import PromptVersioner, VersionBump
import time
import random

# Multi-stage code review system
pv = PromptVersioner("code-review-ai")

# Stage 1: Security Analysis
pv.save_version(
    name="security_reviewer",
    system_prompt="""You are a cybersecurity expert specializing in code review.
    Focus on identifying security vulnerabilities, authentication issues, and
    data exposure risks.""",
    user_prompt="""Analyze this code for security vulnerabilities:
    {language}
    {code}
    Security Analysis:
    1. Vulnerabilities Found:
    2. Risk Level (High/Medium/Low):
    3. Recommendations:""",
    bump_type=VersionBump.MAJOR,
    metadata={"stage": "security", "focus": "vulnerabilities"},
)

# Stage 2: Performance Analysis
pv.save_version(
    name="performance_reviewer",
    system_prompt="""You are a senior software engineer specializing in performance
    optimization. Identify bottlenecks, inefficient algorithms, and scalability issues.""",
    user_prompt="""Review this code for performance issues:
    {language}
    {code}

    Performance Analysis:
    1. Bottlenecks Identified:
    2. Algorithm Complexity:
    3. Optimization Suggestions:""",
    bump_type=VersionBump.MAJOR,
    metadata={"stage": "performance", "focus": "optimization"},
)

# Stage 2: Performance Analysis
pv.save_version(
    name="performance_reviewer",
    system_prompt="""You are a senior software engineer specializing in performance
    optimization. Identify bottlenecks, inefficient algorithms, and scalability issues.""",
    user_prompt="""Review this code for performance issues:
    {language}
    {code}

    Performance Analysis:
    1. Bottlenecks Identified:
    2. Algorithm Complexity:
    3. Optimization Suggestions:""",
    bump_type=VersionBump.MAJOR,
    metadata={"stage": "performance", "focus": "optimization"},
)


def call_llm_with_metrics(prompt_data: dict, user_prompt: str, review_type: str) -> str:
    """
    Call LLM with comprehensive metrics tracking for code review.

    Args:
        prompt_data: Dictionary containing prompt version info
        user_prompt: Formatted user prompt
        review_type: Type of review (security_reviewer, performance_reviewer)

    Returns:
        LLM response as string
    """
    print(f"\n🔍 Starting {review_type} analysis...")
    print(f"   Using prompt version: {prompt_data['version']}")

    # Track timing
    start_time = time.time()

    # Simulate LLM call with realistic responses
    print("   ⏳ Calling LLM...")

    # Simulate processing time based on review type
    processing_time = random.uniform(1.2, 3.5)  # nosec B311
    time.sleep(min(processing_time, 0.1))  # Actually sleep only briefly for demo

    # Generate realistic review responses
    if review_type == "security_reviewer":
        response_content = generate_security_review()
    elif review_type == "performance_reviewer":
        response_content = generate_performance_review()
    else:
        response_content = "Review completed successfully."

    # Calculate metrics
    latency = (time.time() - start_time) * 1000
    input_tokens = len(user_prompt) // 4  # Rough estimation
    output_tokens = len(response_content) // 4

    print(f"   ✅ Review completed in {latency:.1f}ms")
    print(f"   📊 Tokens - Input: {input_tokens}, Output: {output_tokens}")

    # Log metrics to PromptVersioner
    print("   💾 Logging metrics...")
    pv.log_metrics(
        name=review_type,
        version=prompt_data["version"],
        model_name="gpt-4o",
        input_tokens=input_tokens,
        output_tokens=output_tokens,
        latency_ms=latency,
        success=True,
        metadata={
            "review_type": review_type,
            "code_length": len(user_prompt),
            "processing_time": processing_time,
        },
    )
    print("   ✅ Metrics logged successfully")

    return response_content


def generate_security_review() -> str:
    """Generate a realistic security review response."""
    vulnerabilities = [
        "SQL injection vulnerability in database query construction",
        "Unvalidated user input in file upload functionality",
        "Hardcoded API keys in configuration",
        "Missing authentication checks on sensitive endpoints",
        "Insufficient input sanitization for XSS prevention",
    ]

    risk_levels = ["High", "Medium", "Low"]

    selected_vuln = random.choice(vulnerabilities)  # nosec B311
    risk_level = random.choice(risk_levels)  # nosec B311

    return f"""Security Analysis:
1. Vulnerabilities Found:
   - {selected_vuln}
   - Potential data exposure through error messages
   - Missing rate limiting on API endpoints

2. Risk Level: {risk_level}
   - Primary concern: {selected_vuln.lower()}
   - Secondary issues may compound risk

3. Recommendations:
   - Implement parameterized queries to prevent SQL injection
   - Add comprehensive input validation and sanitization
   - Use environment variables for sensitive configuration
   - Implement proper authentication middleware
   - Add rate limiting and request throttling
   - Conduct regular security audits"""


def generate_performance_review() -> str:
    """Generate a realistic performance review response."""
    bottlenecks = [
        "N+1 query problem in database operations",
        "Inefficient loop causing O(n²) complexity",
        "Missing database indexes on frequently queried columns",
        "Synchronous I/O operations blocking main thread",
        "Large object allocations causing garbage collection pressure",
    ]

    complexities = ["O(n²)", "O(n log n)", "O(n)", "O(log n)"]

    selected_bottleneck = random.choice(bottlenecks)  # nosec B311
    complexity = random.choice(complexities)  # nosec B311

    return f"""Performance Analysis:
    1. Bottlenecks Identified:
    - {selected_bottleneck}
    - Redundant computations in hot code paths
    - Inefficient data structure usage

    2. Algorithm Complexity: {complexity}
    - Current implementation shows {complexity.lower()} time complexity
    - Memory usage could be optimized

    3. Optimization Suggestions:
    - Implement caching for frequently accessed data
    - Use batch operations for database queries
    - Add appropriate database indexes
    - Consider asynchronous processing for I/O operations
    - Optimize data structures for better cache locality
    - Profile code to identify actual bottlenecks in production"""


# Integrated review function
def comprehensive_code_review(code: str, language: str):
    """Run multi-stage code review with metrics tracking."""
    print(f"\n🔍 Starting comprehensive code review for {language} code...")
    print(f"   Code length: {len(code)} characters")
    print("=" * 60)

    reviews = {}

    for review_type in ["security_reviewer", "performance_reviewer"]:
        prompt_data = pv.get_latest(review_type)

        # Format and execute
        formatted_prompt = prompt_data["user_prompt"].format(code=code, language=language)

        review_result = call_llm_with_metrics(
            prompt_data=prompt_data, user_prompt=formatted_prompt, review_type=review_type
        )

        reviews[review_type] = review_result
        print(f"\n📋 {review_type.replace('_', ' ').title()} Results:")
        print("-" * 40)
        print(review_result)

    return reviews


# Example usage
if __name__ == "__main__":
    print("🚀 Code Review AI System")
    print("=" * 50)

    # Sample code to review
    sample_code = """
def login_user(username, password):
    query = f"SELECT * FROM users WHERE username='{username}' AND password='{password}'"
    result = db.execute(query)

    if result:
        for user in get_all_users():  # N+1 query problem
            if user.username == username:
                return create_session(user)

    return None

def get_user_data(user_id):
    # Missing input validation
    data = []
    for i in range(1000):
        for j in range(1000):  # O(n²) complexity
            if should_include(i, j, user_id):
                data.append(process_data(i, j))
    return data
"""

    # Run comprehensive review
    results = comprehensive_code_review(sample_code, "Python")

    print("\n📊 Review Summary:")
    print("=" * 50)
    print("✅ Security review completed")
    print("✅ Performance review completed")
    print("📈 All metrics logged to PromptVersioner")

    # Show available prompts and their metrics
    print("\n📋 Available Review Types:")
    for prompt_name in pv.list_prompts():
        versions = pv.list_versions(prompt_name)
        for version in versions:
            v = pv.get_version(prompt_name, version["version"])
            metrics_count = len(pv.storage.get_metrics(version["id"]))
            print(f"   {prompt_name} v{version['version']}: {metrics_count} reviews logged")
