def evaluate(user_attributes, feature_definition):
    """ Evaluate whether a user with given attributes has access to a feature.
    Right now, multi-variate configuration is not supported, so boolean would 
    suffice.

    so, only a boolean should suffice. 
    :param user_attributes: user's attributes in a dictionary
    :type user_attributes: dict

    :param feature_definition: the feature to evaluate against
    :type feature_definition: FeatureDefinition

    :return: Access status true/false for the feature key and user attributes.
    :rtype: bool
    """

    