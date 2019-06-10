
import random

class Distribution(object):
  def __init__(self, rand_args, rand_fn):
    self._args = rand_args
    self._fn = rand_fn

  def Next(self):
    return getattr(random, self._fn)(*self._args)


class Uniform(Distribution):
  def __init__(self, center, delta):
    super().__init__([center-delta, center+delta], 'uniform')


class Gauss(Distribution):
  def __init__(self, mu, sigma):
    super().__init__([mu, sigma], 'gauss')


class Lgauss(Distribution):
  def __init__(self, mu, sigma):
    super().__init__([mu, sigma], 'lognormvariate')


class Pareto(Distribution):
  def __init__(self, alpha):
    super().__init__([alpha], 'paretovariate')


class Value(Distribution):
  def __init__(self, val):
    self._val = val

  def Next(self):
    return self._val


class Matches(object):
  def __init__(self, *wants):
    self._wants = wants

  def Snapshot(self):
    class MSnap(object):
      def __init__(self, snaps):
        self._snaps = snaps

      def GetValueFor(self, val):
        v = self._snaps.get(val)
        if v:
          return v.GetValueFor(val)
        return 0

      def __repr__(self):
        return str(list(self._snaps.values()))

    return MSnap({w._value:w.Snapshot() for w in self._wants})


class Wants(object):
  def __init__(self, value, at):
    self._value = value
    self._dist = at

  def Snapshot(self):
    class Snapshot(object):
      def __init__(self, value, price):
        self._value = value
        self._price = price

      def GetValueFor(self, val):
        if val == self._value:
          return self._price
        return 0

      def __repr__(self):
        return '{{{}: ${:.2f}}}'.format(self._value, self._price)

    return Snapshot(self._value, self._dist.Next())


class SampleGroup(object):
  def __init__(self, value_preferences=None):
    self._vprefs = value_preferences or {}
    random.seed()

  def TestPreference(self, survey):
    a = survey.NextCombination()
    b = survey.NextCombination()

    # if this is > 0, there is a preference for A!
    preference_for_a = b.price - a.price
    prefs = []

    for key, pref in self.GetPreferenceSnapshot():
      preference_for_a += pref.GetValueFor(a[key])
      preference_for_a -= pref.GetValueFor(b[key])
      prefs.append([key, pref])

    if preference_for_a > 0:
      return prefs, a, b
    else:
      return prefs, b, a

  def GetPreferenceSnapshot(self):
    for key, wants in self._vprefs.items():
      yield key, wants.Snapshot()


def RunSurveyOnSamplePop(popsize, population, survey, exclude=None):
  exclude = exclude or []
  result = {l:{} for l in survey._variables.keys() if l not in exclude}
  for _ in range(popsize):
    _, win, lose = population.TestPreference(survey)
    for key in result:
      val = getattr(win, key)
      if val not in result[key]:
        result[key][val] = 1
      else:
        result[key][val] += 1
  return result
