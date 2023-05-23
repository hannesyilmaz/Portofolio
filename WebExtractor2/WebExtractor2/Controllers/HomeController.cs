using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Linq;
using WebExtractor2.Models;
using System.Diagnostics;
using MySql.Data.MySqlClient;
using System.Globalization;
using MongoDB.Driver.Builders;

namespace WebExtractor2.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index(string topic, string sortBy)
        {
            // Get all articles from the database
            List<ArticleModel> allArticles = GetArticlesFromDatabase();

            // Get all the unique topics from the articles
            List<string> allTopics = allArticles.SelectMany(article => article.Topic.Split(',')).Distinct().ToList();

            // Filter the articles by topic if a specific topic is selected
            if (!string.IsNullOrEmpty(topic))
            {
                allArticles = allArticles.Where(article => article.Topic.Contains(topic)).ToList();
            }

            // Sort the articles by published date based on the selected sorting option
            switch (sortBy)
            {
                case "newest":
                    allArticles = allArticles.OrderByDescending(article => article.Published).ToList();
                    break;
                case "oldest":
                    allArticles = allArticles.OrderBy(article => article.Published).ToList();
                    break;
                default:
                    break;
            }

            // Pass the list of ArticleModel objects, the selected topic, the selected sorting option, and the list of all topics to the view to be displayed
            ViewBag.SelectedTopic = topic;
            ViewBag.SelectedSortBy = sortBy;
            ViewBag.AllTopics = allTopics;
            return View(allArticles);
        }



        private List<ArticleModel> GetArticlesFromDatabase(bool ascending = true)
        {
            // Connection string for MySQL database
            string connStr = "server=localhost;user=root;database=newsextractdb;port=3306;password=Hs02209374%"; 

            // SQL query to retrieve data from database
            string sql = "SELECT title, summary, link, published, topic FROM news";

            // Create a list to hold ArticleModel objects
            List<ArticleModel> articles = new List<ArticleModel>();

            using (MySqlConnection conn = new MySqlConnection(connStr))
            {
                using (MySqlCommand cmd = new MySqlCommand(sql, conn))
                {
                    conn.Open();
                    using (MySqlDataReader reader = cmd.ExecuteReader())
                    {
                        // Loop through each row in the result set and create an ArticleModel object from the data
                        while (reader.Read())
                        {
                            ArticleModel article = new ArticleModel();
                            article.Title = reader.GetString("title");
                            article.Summary = reader.GetString("summary");
                            article.Link = reader.GetString("link");
                            article.Published = reader.GetDateTime("published");
                            article.Topic = reader.GetString("topic");

                            articles.Add(article);
                        }
                    }
                }
            }

            return articles;
        }



        public IActionResult Privacy()
        {
            return View();
        }

        [ResponseCache(Duration = 0, Location = ResponseCacheLocation.None, NoStore = true)]
        public IActionResult Error()
        {
            return View(new ErrorViewModel { RequestId = Activity.Current?.Id ?? HttpContext.TraceIdentifier });
        }
    }
}
