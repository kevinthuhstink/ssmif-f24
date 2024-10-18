""" The custom asset returns model. """

import cvxpy as cp
import pandas as pd
from .factors import FactorModel, risk_free_rates


class Carhart4FactorModel:
    """ Custom Carhart 4-factor model """
    def __init__(self):
        self.reconstruct_factors()

    def __call__(self, rates):
        """ Applies the Carhart model onto the given asset.

        :param rates: Annualized return rates for the asset.
        :type rates: pandas.Series, indexed by pandas.Timestamp

        :return: Expected future rate of return for the asset
        :rtype: float
        """
        days_with_data = rates.index.intersection(self.factors.index)
        factors = self.factors.loc[days_with_data].to_numpy()
        asset_returns = rates.loc[days_with_data].to_numpy()
        risk_free = self.risk_free_rates.loc[days_with_data].to_numpy()

        betas = cp.Variable(4) # [ bCAPM, bSMB, bHML, bUMD ]
        objective = cp.Minimize(cp.sum_squares(factors @ betas + risk_free - asset_returns))
        cp.Problem(objective).solve()

        curr_factors = factors[-1]
        curr_rfrate = risk_free[-1]
        return betas.value.dot(curr_factors) + curr_rfrate

    def reconstruct_factors(self):
        """ Constructs the factors used in the 4-factor model.
        Each factor has 253 entries corresponding to the last 253 trading days.
        Should only be used when we have a new trading day the old model didn't account for.
        """
        updated_model = FactorModel()
        self.factors = pd.concat([
            updated_model.mkt_premium(),
            updated_model.smb(),
            updated_model.hml(),
            updated_model.umd()
            ], axis=1)
        self.risk_free_rates = risk_free_rates()
