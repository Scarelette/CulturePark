
culture_dict = {'Arabic': {'people': 'Arabian', 'boy': 'Abdul', 'girl': 'Fatima'},
                'Bengali': {'people': 'Bengali', 'boy': 'Aarav', 'girl': 'Ananya'},
                'Chinese': {'people': 'Chinese', 'boy': 'Wei', 'girl': 'Lili'},
                'Germany': {'people': 'German', 'boy': 'Maximilian', 'girl': 'Sophia'},
                'Korean': {'people': 'Korean', 'boy': 'Joon', 'girl': 'Haeun'},
                'Portuguese': {'people': 'Portuguese', 'boy': 'João', 'girl': 'Maria'},
                'Spanish': {'people': 'Spanish', 'boy': 'Javier', 'girl': 'María'},
                'Turkish': {'people': 'Turkish', 'boy': 'Mehmet', 'girl': 'Ayşe'}}

vsm13_data = {'1': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nhave sufficient time for your personal or home life',
              '2': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nhave a boss (direct superior) you can respect',
              '3': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nget recognition for good performance',
              '4': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nhave security of employment',
              '5': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nhave pleasant people to work with',
              '6': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\ndo work that is interesting',
              '7': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nbe consulted by your boss in decisions involving your work',
              '8': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nlive in a desirable area',
              '9': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nhave a job respected by your family and friends',
              '10': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn choosing an ideal job, how important would it be to you to:\nhave chances for promotion',
              '11': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn your private life, how important is each of the following to you: (please circle one answer in each line across):\nkeeping time free for fun',
              '12': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn your private life, how important is each of the following to you: (please circle one answer in each line across):\nmoderation: having few desires',
              '13': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn your private life, how important is each of the following to you: (please circle one answer in each line across):\ndoing a service to a friend',
              '14': 'Answer the questions below by choosing an answer from the following: 1 = of utmost importance, 2 = very important, 3 = of moderate importance, 4 = of little importance, 5 = of very little or no importance\nIn your private life, how important is each of the following to you: (please circle one answer in each line across):\nthrift (not spending more than needed)',
              '15': 'Answer the questions below by choosing an answer from the following: 1 = always, 2 = usually, 3 = sometimes, 4 = seldom, 5 = never\nHow often do you feel nervous or tense?',
              '16': 'Answer the questions below by choosing an answer from the following: 1 = always, 2 = usually, 3 = sometimes, 4 = seldom, 5 = never\nAre you a happy person?',
              '17': 'Answer the questions below by choosing an answer from the following: 1 = yes, always, 2 = yes, usually, 3 = sometimes, 4 = no, seldom, 5 = no, never\nDo other people or circumstances ever prevent you from doing what you really want to?',
              '18': 'Answer the questions below by choosing an answer from the following: 1 = very good, 2 = good, 3 = fair, 4 = poor, 5 = very poor\nAll in all, how would you describe your state of health these days?',
              '19': 'Answer the questions below by choosing an answer from the following: 1 = very proud, 2 = fairly proud, 3 = somewhat proud, 4 = not very proud, 5 = not proud at all\nHow proud are you to be a citizen of your country?',
              '20': 'Answer the questions below by choosing an answer from the following: 1 = never, 2 = seldom, 3 = sometimes, 4 = usually, 5 = always\nHow often, in your experience, are subordinates afraid to contradict their boss (or students their teacher?)',
              '21': 'Answer the questions below by choosing an answer from the following: 1 = strongly agree, 2 = agree, 3 = undecided, 4 = disagree, 5 = strongly disagree\nTo what extent do you agree or disagree with each of the following statements?:\nOne can be a good manager without having a precise answer to every question that a subordinate may raise about his or her work',
              '22': 'Answer the questions below by choosing an answer from the following: 1 = strongly agree, 2 = agree, 3 = undecided, 4 = disagree, 5 = strongly disagree\nTo what extent do you agree or disagree with each of the following statements?:\nPersistent efforts are the surest way to results',
              '23': 'Answer the questions below by choosing an answer from the following: 1 = strongly agree, 2 = agree, 3 = undecided, 4 = disagree, 5 = strongly disagree\nTo what extent do you agree or disagree with each of the following statements?:\nAn organization structure in which certain subordinates have two bosses should be avoided at all cost',
              '24': 'Answer the questions below by choosing an answer from the following: 1 = strongly agree, 2 = agree, 3 = undecided, 4 = disagree, 5 = strongly disagree\nTo what extent do you agree or disagree with each of the following statements?:\nA company\'s or organization\'s rules should not be broken - not even when the employee thinks breaking the rule would be in the organization\'s best interest'}

model_dict = {'Arabic': '',
                'Bengali': '',
                'Chinese': '',
                'Germany': '',
                'Korean': '',
                'Portuguese': '',
                'Spanish': '',
                'Turkish': ''}