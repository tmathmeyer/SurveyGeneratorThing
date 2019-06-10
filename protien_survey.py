
import libsurvey


SUSTAINABILITY_CERTIFICATION_VALUE_ADDED = 1.00
FREE_RANGE_WILD_VALUE_ADD = 1.50
FRESHNESS_VALUE_ADD = 2.00
PNW_ORIGIN_VALUE_ADD = 1.00
USA_ORIGIN_VALUE_ADD = 0.60
ABROAD_ORIGIN_VALUE_ADD = 0
MEAT_BASE_VALUE = {
  'Chicken': 11.00,
  'Beef': 13.00,
  'Salmon': 15.00,
  'Trout': 13.10,
  'Sushi': 17.00
}

class PremiumPriceCalculator(libsurvey.Calculation):
  @classmethod
  def CalculateValue(cls, survey):
    base_price = MEAT_BASE_VALUE[survey.meat]
    certification_value = (
      SUSTAINABILITY_CERTIFICATION_VALUE_ADDED if survey.certification else 0)
    production_value = (
      0 if survey.production == 'Farmed' else FREE_RANGE_WILD_VALUE_ADD)
    fresh_value = (
      FRESHNESS_VALUE_ADD if survey.fresh else 0)
    origin_value = {
      'PNW': PNW_ORIGIN_VALUE_ADD,
      'USA': USA_ORIGIN_VALUE_ADD,
      'Abroad': ABROAD_ORIGIN_VALUE_ADD,
    }[survey.origin]
    return (
      base_price +
      certification_value +
      production_value +
      fresh_value +
      origin_value)


MEAT_SURVEY = libsurvey.RandomSurvey(
  meat=libsurvey.Choice('Meat', ['Chicken', 'Beef', 'Salmon', 'Trout', 'Sushi']),
  certification=libsurvey.Type('Sustainability Certification', bool),
  production=libsurvey.Choice('Production Method', ['Freerange/Wild', 'Farmed']),
  fresh=libsurvey.Type('Fresh (Not Frozen)', bool),
  origin=libsurvey.Choice('Origin', ['PNW', 'USA', 'Abroad']),
  price=libsurvey.Calculation('Price', PremiumPriceCalculator))
