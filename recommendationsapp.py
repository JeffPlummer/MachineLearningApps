import webapp2
import os
from jinja2 import Environment, FileSystemLoader


from net.jeffplummer.recommendations import recommendations
from net.jeffplummer.recommendations import recommendations_web
#from net.jeffplummer.recommendations.deliciousrec import *

env = jinja_environment=Environment(autoescape=True, extensions=['jinja2.ext.autoescape'],
                  loader=FileSystemLoader(os.path.dirname(__file__)))

template_values = {
      'formatted_data': recommendations_web.criticsAsHTMLTable()
      }

class MovieDataPage(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template("SampleData.html")
    self.response.out.write(template.render(template_values))
 
class MainPage(webapp2.RequestHandler):
  def get(self):
     
    if(self.request.get('func')):
      self.displayFunctionResults()
      
    template = jinja_environment.get_template("main.html")
    self.response.out.write(template.render(template_values))
      
  def displayFunctionResults(self):
      func = self.request.get('func')
      if func == 'criticSimilarity': 
        topEuclid = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_euclid_distance)
        template_values['resultEuclidean'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topEuclid)
        topPearson = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_pearson_distance)
        template_values['resultPearson'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topPearson)
        topCos = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_cosine)
        template_values['resultCosine'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topCos)
        topExtJaccard = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_ext_jaccard)
        template_values['resultExtJaccard'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topExtJaccard)
        
        
      elif func == 'getRecommendation':
        recommends = recommendations.getRecommendations(recommendations.critics, 
                        self.request.get('criticToGetRecommendations'))
        template_values['result'] = recommendations_web.tupleAsHTMLTable(['Likability Rating', 'Movie Title'], recommends)
      elif func == 'getSimilarMovies':
        movies = recommendations.transformPrefs(recommendations.critics)
        recommends = recommendations.topMatches(movies, 
                        self.request.get('movieToGetSimilar'))
        template_values['result'] = recommendations_web.tupleAsHTMLTable(['Recommendation Rating', 'Movie Title'], recommends)
        
      
class CriticSimilarity(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template("/html/CompareCritics.html")
    
    if  self.request.get('criticToCompare') != "":
      topEuclid = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_euclid_distance)
      template_values['resultEuclidean'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topEuclid)
      topPearson = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_pearson_distance)
      template_values['resultPearson'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topPearson)
      topCos = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_cosine)
      template_values['resultCosine'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topCos)
      topExtJaccard = recommendations.topMatches(recommendations.critics, 
                        self.request.get('criticToCompare'), -1, recommendations.similarities_ext_jaccard)
      template_values['resultExtJaccard'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topExtJaccard)
    
    self.response.out.write(template.render(template_values))
          
class ItemSimilarity(webapp2.RequestHandler):
  def get(self):
    template = jinja_environment.get_template("/html/CompareItems.html")
    
    itemToCompare = self.request.get('itemToCompare')
    if itemToCompare  != "":
      topEuclid = recommendations.topMatches(recommendations.critics, 
                        itemToCompare, -1, recommendations.similarities_euclid_distance)
      template_values['resultEuclidean'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topEuclid)
      topPearson = recommendations.topMatches(recommendations.critics, 
                        itemToCompare, -1, recommendations.similarities_pearson_distance)
      template_values['resultPearson'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topPearson)
      topCos = recommendations.topMatches(recommendations.critics, 
                        itemToCompare, -1, recommendations.similarities_cosine)
      template_values['resultCosine'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topCos)
      topExtJaccard = recommendations.topMatches(recommendations.critics, 
                        itemToCompare, -1, recommendations.similarities_ext_jaccard)
      template_values['resultExtJaccard'] = recommendations_web.tupleAsHTMLTable(['Similarity', 'Critic'], topExtJaccard)
    
    self.response.out.write(template.render(template_values))
    
class test(webapp2.RequestHandler):
  def get(self):
    recommendations.similarities_euclid_distance(recommendations.critics, 'Bob', 'Larry')
  
  
app = webapp2.WSGIApplication([('/', test),
                               ('/MovieData', MovieDataPage),
                               ('/CompareMovieCritics', CriticSimilarity),
                               ('/MoviesExample', MainPage)],
                              debug=True)