import numpy as np
from flask import Flask, request, jsonify, render_template
import pickle

app = Flask(__name__) #Initialize the flask App
model = pickle.load(open( "word2vec_trained.p", "rb" ))
model_prep_modes = pickle.load( open( "ingredients_prep_modes_50000_2.pkl", "rb" ) )

#This tells what to do when the app is started. -> Redirect to our start html (index.html)
@app.route('/')
def home():
    return render_template('index.html')


#This is where it reads out the given input and predicts
@app.route('/predict',methods=['POST'])
def predict():
    '''
    For rendering results on HTML GUI
    '''
    #get the featrues out of feature form
    my_list = list([str(x) for x in request.form.values()])
    main = my_list[0]
    my_list = my_list[1:]
    
    #Now we have to run find the proper ingredience
    def choose_ingredients(main, ingredient_list):
    '''Takes a main ingredient and a list of ingredients. 
    Gives back a list of chosen ingredients based on cosine similarities, which are calculated against the main ingredient'''
    chosen_ingredients = []
    for ingredient in ingredient_list:
        try:
            similarity = 1 - distance.cosine(model.wv[main], model.wv[ingredient])
            if similarity > 0:
                chosen_ingredients.append(ingredient)

        except:
            print('Seems like {0} is not in our database! It will not be featured in our recipe. Sorry about that!'.format(ingredient))
            pass

    return chosen_ingredients

    
    chosen_ingredients = choose_ingredients(main, my_list)

    #Now its time to see the prep_modes
    def get_prep_modes(ingredients_chosen):
    '''Takes chosen ingredients and returns preparation modes for them.'''
    print('To follow your delicious recipe please: \n')
    for ingredient in ingredients_chosen:
        try:
            instructions = list(model_prep_modes.get(ingredient).keys())[0:3]
            print('{0} and/or {1} the {2}'.format(instructions[0], instructions[1], ingredient))

        except:
            print('Seems like {0} is not in our database! It will not be featured in our recipe. Sorry about that!'.format(ingredient))
            pass

    get_prep_modes(chosen_ingredients)



#Following has to be adjusted accoring to our code and environment

    return render_template('index.html', prediction_text='Employee Salary should be $ {}'.format(output))

if __name__ == "__main__":
    app.run(debug=True)
