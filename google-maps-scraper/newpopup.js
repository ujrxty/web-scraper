function scrapeData() {
    var links = Array.from(document.querySelectorAll('a[href^="https://www.google.com/maps/place"]'));
    return Promise.all(links.map(link => {
        var container = link.closest('[jsaction*="mouseover:pane"]');
        var titleText = container ? container.querySelector('.fontHeadlineSmall').textContent : '';
        var rating = '';
        var reviewCount = '';
        var phone = '';
        var industry = '';
        var address = '';
        var companyUrl = '';
        var email = ''; // New field for email

        // Rating and Reviews
        if (container) {
            var roleImgContainer = container.querySelector('[role="img"]');
            
            if (roleImgContainer) {
                var ariaLabel = roleImgContainer.getAttribute('aria-label');
            
                if (ariaLabel && ariaLabel.includes("stars")) {
                    var parts = ariaLabel.split(' ');
                    rating = parts[0];
                    reviewCount = '(' + parts[2] + ')'; 
                } else {
                    rating = '0';
                    reviewCount = '0';
                }
            }
        }

        // Address and Industry
        if (container) {
            var containerText = container.textContent || '';
            var addressRegex = /\d+ [\w\s]+(?:#\s*\d+|Suite\s*\d+|Apt\s*\d+)?/;
            var addressMatch = containerText.match(addressRegex);

            if (addressMatch) {
                address = addressMatch[0];

                // Extract industry text based on the position before the address
                var textBeforeAddress = containerText.substring(0, containerText.indexOf(address)).trim();
                var ratingIndex = textBeforeAddress.lastIndexOf(rating + reviewCount);
                if (ratingIndex !== -1) {
                    var rawIndustryText = textBeforeAddress.substring(ratingIndex + (rating + reviewCount).length).trim().split(/[\r\n]+/)[0];
                    industry = rawIndustryText.replace(/[·.,#!?]/g, '').trim();
                }
                var filterRegex = /\b(Closed|Open 24 hours|24 hours)|Open\b/g;
                address = address.replace(filterRegex, '').trim();
                address = address.replace(/(\d+)(Open)/g, '$1').trim();
                address = address.replace(/(\w)(Open)/g, '$1').trim();
                address = address.replace(/(\w)(Closed)/g, '$1').trim();
            } else {
                address = '';
            }
        }

        // Company URL
        if (container) {
            var allLinks = Array.from(container.querySelectorAll('a[href]'));
            var filteredLinks = allLinks.filter(a => !a.href.startsWith("https://www.google.com/maps/place/"));
            if (filteredLinks.length > 0) {
                companyUrl = filteredLinks[0].href;
            }
        }

        // Phone Numbers
        if (container) {
            var containerText = container.textContent || '';
            var phoneRegex = /(\+\d{1,2}\s)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}/;
            var phoneMatch = containerText.match(phoneRegex);
            phone = phoneMatch ? phoneMatch[0] : '';
        }

        // Fetch email from the company website
        if (companyUrl) {
            return fetchEmailFromWebsite(companyUrl).then(fetchedEmail => {
                email = fetchedEmail;
                return {
                    title: titleText,
                    rating: rating,
                    reviewCount: reviewCount,
                    phone: phone,
                    industry: industry,
                    address: address,
                    companyUrl: companyUrl,
                    href: link.href,
                    email: email // Include email in the returned object
                };
            });
        } else {
            return Promise.resolve({
                title: titleText,
                rating: rating,
                reviewCount: reviewCount,
                phone: phone,
                industry: industry,
                address: address,
                companyUrl: companyUrl,
                href: link.href,
                email: email // Include email in the returned object
            });
        }
    }));
}

// Function to fetch email from the website
function fetchEmailFromWebsite(url) {
    return fetch(url)
        .then(response => {
            if (!response.ok) throw new Error('Network response was not ok');
            return response.text();
        })
        .then(html => {
            // Use a regex to find email addresses in the HTML
            const emailRegex = /[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}/g;
            const emails = html.match(emailRegex);
            return emails ? emails[0] : ''; // Return the first email found or an empty string
        })
        .catch(() => {
            return ''; // Return an empty string if there's an error
        });
}
