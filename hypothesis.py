
import libhypothesis
import protien_survey

# Codify the hypothesis!
# NOTE: these values can be DIFFERENT than the values in protien_survey.py
# Those values are meant to be guesses, even NONSENSE, UNINFORMED guesses.
# The idea is that even with bad guesses, the random survey should be
# able to deduce the real world values which are shown here.

# A scenario contains some set of (name, distribution) pairs, where supported
# distributions are:
#   Uniform distribution:   Uniform(average, +-Delta)
#   Gauss distribution:     Gauss(average, sigma)
#   lognormal distribution: Lgauss(average, sigma)
#   pareto distribution:    Pareto(alpha)
#   fixed distribution:     Value(value)

# Wants are described as either:
#   Wants:   a pair of value, distribution, or
#   Matches: a list Wants




# Hypothesis 1:
# The average person values _any_ freshness at gauss(avg=0.60, sigma=0.2), and
# freerange / wild over farmed at gauss(avg=0.10, sigma=0.2).
population1 = libhypothesis.SampleGroup(
  value_preferences={
    'fresh': libhypothesis.Wants(
      value=True,
      at=libhypothesis.Uniform(1.00, 0.80)),
    'production': libhypothesis.Wants(
      value='Freerange/Wild',
      at=libhypothesis.Gauss(0.10, 0.20)),
    'meat': libhypothesis.Matches(
      libhypothesis.Wants(
        value='Chicken',
        at=libhypothesis.Gauss(10.50, 1.00)),
      libhypothesis.Wants(
        value='Beef',
        at=libhypothesis.Gauss(14.10, 3.00)),
      libhypothesis.Wants(
        value='Salmon',
        at=libhypothesis.Gauss(16.00, 6.00)),
      libhypothesis.Wants(
        value='Trout',
        at=libhypothesis.Gauss(16.00, 6.10)),
      libhypothesis.Wants(
        value='Sushi',
        at=libhypothesis.Gauss(19.00, 7.00))),
    'certification': libhypothesis.Wants(
      value=True,
      at=libhypothesis.Value(0.10)),
    'origin': libhypothesis.Matches(
      libhypothesis.Wants(
        value='PNW',
        at=libhypothesis.Value(0.20)),
      libhypothesis.Wants(
        value='USA',
        at=libhypothesis.Value(0.05)),
      libhypothesis.Wants(
        value='Abroad',
        at=libhypothesis.Value(-0.10)))
  })

# Note that in this population, people have exactly the same preferences as
# were guessed when making the sample - what a coincidence!
# Actually this is just interesting to compare the results with the pop1.
# Data from the survey:
"""
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
"""
population2 = libhypothesis.SampleGroup(
  value_preferences={
    'fresh': libhypothesis.Wants(
      value=True,
      at=libhypothesis.Uniform(2.00, 0.50)),
    'production': libhypothesis.Wants(
      value='Freerange/Wild',
      at=libhypothesis.Gauss(1.50, 0.50)),
    'meat': libhypothesis.Matches(
      libhypothesis.Wants(
        value='Chicken',
        at=libhypothesis.Gauss(11.00, 1.00)),
      libhypothesis.Wants(
        value='Beef',
        at=libhypothesis.Gauss(13.00, 1.00)),
      libhypothesis.Wants(
        value='Salmon',
        at=libhypothesis.Gauss(15.00, 1.00)),
      libhypothesis.Wants(
        value='Trout',
        at=libhypothesis.Gauss(13.10, 1.00)),
      libhypothesis.Wants(
        value='Sushi',
        at=libhypothesis.Gauss(17.00, 1.00))),
    'certification': libhypothesis.Wants(
      value=True,
      at=libhypothesis.Value(1.00)),
    'origin': libhypothesis.Matches(
      libhypothesis.Wants(
        value='PNW',
        at=libhypothesis.Value(1.00)),
      libhypothesis.Wants(
        value='USA',
        at=libhypothesis.Value(0.60)),
      libhypothesis.Wants(
        value='Abroad',
        at=libhypothesis.Value(0.00)))
  })



def main():
  print('population1, samplesize 50000:')
  values = libhypothesis.RunSurveyOnSamplePop(
    50000, population1, protien_survey.MEAT_SURVEY, exclude=['price'])
  print(values)
  print('')
  print('population2, samplesize 50000:')
  values = libhypothesis.RunSurveyOnSamplePop(
    50000, population2, protien_survey.MEAT_SURVEY, exclude=['price'])
  print(values)



main()