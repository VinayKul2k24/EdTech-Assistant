from rag import setup_rag, get_rag_answer


class PlannerAgent:
    def decide_agent(self, query: str) -> str:
        query_lower = query.lower()
        if "practice" in query_lower or "question" in query_lower:
            return "practice_generator"
        elif "explain" in query_lower or "what is" in query_lower:
            return "tutor"
        else:
            return "general"


class TutorAgent:
    def __init__(self, vector_db):
        self.vector_db = vector_db

    def explain_concept(self, query: str) -> str:
        return get_rag_answer(query, self.vector_db)


class PracticeGeneratorAgent:
    def generate_practice(self, topic: str) -> str:
        return f"Practice questions about {topic}:\n1. Question 1\n2. Question 2\n3. Question 3"


class Assistant:
    def __init__(self):
        self.vector_db = setup_rag()
        self.planner = PlannerAgent()
        self.tutor = TutorAgent(self.vector_db)
        self.practice_gen = PracticeGeneratorAgent()

    def handle_query(self, query: str) -> tuple[str, str]:
        agent_name = self.planner.decide_agent(query)

        if agent_name == "tutor":
            response = self.tutor.explain_concept(query)
        elif agent_name == "practice_generator":
            response = self.practice_gen.generate_practice(query)
        else:
            response = "I can help with explanations or practice questions!"

        return response, agent_name