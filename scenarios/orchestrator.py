from typing import Dict, Any, Optional
from loguru import logger


class ScenarioOrchestrator:
    """Orchestrator for managing scenarios."""
    
    def __init__(self, scenarios=None):
        """
        Initialize the scenario orchestrator.
        
        Args:
            scenarios (Optional[Dict]): Dictionary of scenario instances
        """
        self.scenarios = scenarios or {}
        self.active_scenarios = {}  # user_id -> {scenario_name, context}
        logger.info("Scenario orchestrator initialized")
    
    def register_scenario(self, name: str, scenario):
        """
        Register a scenario with the orchestrator.
        
        Args:
            name (str): Name of the scenario
            scenario: Scenario instance
        """
        self.scenarios[name] = scenario
        logger.info(f"Registered scenario: {name}")
    
    async def start_scenario(self, scenario_name: str, user_id: int, context: Dict[str, Any] = None) -> Dict[str, Any]:
        """
        Start a scenario for a user.
        
        Args:
            scenario_name (str): Name of the scenario to start
            user_id (int): User ID
            context (Optional[Dict[str, Any]]): Initial context
            
        Returns:
            Dict[str, Any]: Updated context
        """
        if scenario_name not in self.scenarios:
            logger.error(f"Scenario not found: {scenario_name}")
            return {"error": "Scenario not found"}
        
        # Initialize context if not provided
        if context is None:
            context = {}
        
        # Add scenario info to context
        context["scenario_name"] = scenario_name
        
        # Start the scenario
        scenario = self.scenarios[scenario_name]
        updated_context = await scenario.start(context)
        
        # Check if the scenario is completed
        if not updated_context.get("completed", False):
            # Save active scenario for the user
            self.active_scenarios[user_id] = {
                "scenario_name": scenario_name,
                "context": updated_context
            }
            logger.info(f"Started scenario {scenario_name} for user {user_id}")
        else:
            # Remove active scenario if completed
            if user_id in self.active_scenarios:
                del self.active_scenarios[user_id]
            logger.info(f"Completed scenario {scenario_name} for user {user_id}")
        
        return updated_context
    
    async def process_update(self, user_id: int, update_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Process an update from a user.
        
        Args:
            user_id (int): User ID
            update_data (Dict[str, Any]): Update data
            
        Returns:
            Dict[str, Any]: Updated context
        """
        # Check if user has an active scenario
        if user_id not in self.active_scenarios:
            logger.warning(f"No active scenario for user {user_id}")
            return {"error": "No active scenario"}
        
        # Get active scenario info
        active_scenario = self.active_scenarios[user_id]
        scenario_name = active_scenario["scenario_name"]
        context = active_scenario["context"]
        
        # Process update with the scenario
        scenario = self.scenarios[scenario_name]
        updated_context = await scenario.next_step(context, update_data)
        
        # Update active scenario context
        self.active_scenarios[user_id]["context"] = updated_context
        
        # Check if the scenario is completed
        if updated_context.get("completed", False):
            # Remove active scenario
            del self.active_scenarios[user_id]
            logger.info(f"Completed scenario {scenario_name} for user {user_id}")
        
        return updated_context
    
    async def cancel_scenario(self, user_id: int) -> Dict[str, Any]:
        """
        Cancel the active scenario for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            Dict[str, Any]: Final context after cancellation
        """
        # Check if user has an active scenario
        if user_id not in self.active_scenarios:
            logger.warning(f"No active scenario for user {user_id}")
            return {"error": "No active scenario"}
        
        # Get active scenario info
        active_scenario = self.active_scenarios[user_id]
        scenario_name = active_scenario["scenario_name"]
        context = active_scenario["context"]
        
        # Cancel the scenario
        scenario = self.scenarios[scenario_name]
        final_context = await scenario.cancel(context)
        
        # Remove active scenario
        del self.active_scenarios[user_id]
        logger.info(f"Cancelled scenario {scenario_name} for user {user_id}")
        
        return final_context
    
    def get_active_scenario(self, user_id: int) -> Optional[Dict[str, Any]]:
        """
        Get the active scenario for a user.
        
        Args:
            user_id (int): User ID
            
        Returns:
            Optional[Dict[str, Any]]: Active scenario info if exists, None otherwise
        """
        return self.active_scenarios.get(user_id)