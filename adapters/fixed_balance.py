class FixedBalance:
    def __init__(self, config):
        """
        Initialize with a config dictionary containing fixed balance entries
        
        Args:
            config (dict): Dictionary mapping entry names to USD values
        """
        self.balances = config['fixed_balances']

    def get_fixed_balances(self):
        """
        Returns list of tuples containing (entry_name, usd_value) for each fixed balance
        
        Returns:
            list: List of tuples with (str, float) pairs
        """
        return [(name, value) for name, value in self.balances.items()]
