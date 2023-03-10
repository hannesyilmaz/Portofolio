using Microsoft.AspNetCore.Mvc;
using Microsoft.Extensions.Logging;
using System.Collections.Generic;
using System.Linq;
using WebExtractor2.Models;
using System.Diagnostics;
using MySql.Data.MySqlClient;

namespace WebExtractor2.Controllers
{
    public class HomeController : Controller
    {
        private readonly ILogger<HomeController> _logger;

        public HomeController(ILogger<HomeController> logger)
        {
            _logger = logger;
        }

        public IActionResult Index(string topic)
        {
            // Get all articles from the database
            List<ArticleModel> allArticles = GetArticlesFromDatabase();

            // Filter the articles by topic if a specific topic is selected
            if (!string.IsNullOrEmpty(topic))
            {
                allArticles = allArticles.Where(article => article.Topic.Contains(topic)).ToList();
            }

            // Pass the list of ArticleModel objects and the selected topic to the view to be displayed
            ViewBag.SelectedTopic = topic;
            return View(allArticles);
        }

        private List<ArticleModel> GetArticlesFromDatabase()
        {
            // Connection string for MySQL database
            string connStr = "server=localhost;user=root;database=newsextractdb;port=3306;password=Hs02209374%";

            // SQL query to retrieve data from database
            string sql = "SELECT title, summary, link, published, topic FROM dataset";

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
