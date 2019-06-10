

import random


class Variable(object):
  def __init__(self, name, options):
    self._name = name
    self._options = options
    self._option_count = len(options)

  def Value(self, option):
    assert option < self._option_count
    return self._options[option]

  def OptionCount(self):
    return self._option_count

  def Keyname(self):
    return self._name.split(' ')[0].strip()


class Choice(Variable):
  def __init__(self, name, options):
    super().__init__(name, options)


class Type(Variable):
  def __init__(self, name, clz):
    if clz == bool:
      super().__init__(name, [True, False])
    # TODO(support any enum type!)


class Rank(Variable):
  def __init__(self, name, val):
    super().__init__(name, list(range(val)))


class Calculation(Variable):
  def __init__(self, name, calculator):
    super().__init__(name, [None])
    self._calculator = calculator

  def Value(self, partial_survey_isntance):
    return self._calculator.CalculateValue(partial_survey_isntance)




class Survey(object):
  def __init__(self, **variables):
    self._variables = variables


class RandomSurvey(Survey):
  def __init__(self, **variables):
    super().__init__(**variables)
    random.seed()

  def NextCombination(self):
    values = {}
    calc = (None, None)
    for name, var in self._variables.items():
      if type(var) == Calculation:
        calc = (var, name)
      else:
        select = random.randrange(var.OptionCount())
        values[name] = var.Value(select)
    if calc[0]:
      values[calc[1]] = calc[0].Value(SurveyInstance(**values))
    return SurveyInstance(**values)


class SurveyInstance(object):
  def __init__(self, **variables):
    self.__dict__.update(variables)

  def __getitem__(self, item):
    return self.__dict__[item]

  def __repr__(self):
    return str(self.__dict__)