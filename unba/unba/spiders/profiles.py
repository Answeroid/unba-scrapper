import scrapy
import requests
from concurrent.futures import ThreadPoolExecutor


class ProfilesSpider(scrapy.Spider):
    name = "profiles"
    allowed_domains = ["erau.unba.org.ua"]
    base_url = "https://erau.unba.org.ua/profile"

    def start_requests(self):
        existing_profiles = []

        with ThreadPoolExecutor(max_workers=10) as executor:  # Adjust max_workers as needed
            futures = []

            for profile_number in range(1, 100001):
                url = f"{self.base_url}/{profile_number}"
                future = executor.submit(self.fetch_profile, url, existing_profiles)
                futures.append(future)

            for future in futures:
                result = future.result()
                if result:
                    yield result

        if existing_profiles:
            self.log("Existing Profiles: " + ', '.join(map(str, existing_profiles)))
        else:
            self.log("No existing profiles found.")

    def fetch_profile(self, url, existing_profiles):
        response = requests.get(url)
        if response.status_code == 200 and "На жаль, такої сторінки не існує" not in response.text:
            self.log(f"Profile {url} exists!")
            existing_profiles.append(url)
            return scrapy.Request(url=url, callback=self.parse_profile)

    @staticmethod
    def parse_profile(response):
        yield {
            'profile': response.css('h1.info-about__name::text').get().strip(),
            'accounted': response.css('div.info-about__council-name > h2::text').get().strip(),
            'certificate': response.css('p.info-about__certificate-date::text').get().strip(),
            'cert_date': response.css('div.col-xs-6.col-md-3.info-about__main-secondary > p::text').getall()[3] if len(
                response.css('div.col-xs-6.col-md-3.info-about__main-secondary > p::text').getall()) > 3 else None,
            'cert_auth':
                response.css('div.col-xs-12.col-md-6.info-about__main-secondary.no-border-r > p::text').getall()[
                    1] if len(response.css(
                    'div.col-xs-12.col-md-6.info-about__main-secondary.no-border-r > p::text').getall()) > 1 else None,
            'decision_num': response.css('div.col-xs-6.col-md-3.info-about__main-secondary > p::text').getall()[
                5] if len(
                response.css('div.col-xs-6.col-md-3.info-about__main-secondary > p::text').getall()) > 5 else None,
            'decision_date': response.css('div.col-xs-6.col-md-3.info-about__main-secondary > p::text').getall()[
                7] if len(
                response.css('div.col-xs-6.col-md-3.info-about__main-secondary > p::text').getall()) > 7 else None,
            'total_exp': response.css(
                'div.col-xs-12.col-md-6.info-about__main-secondary.no-border-r::text').get().strip(),
            'term_right_info': response.css('div[data-id]::text').get().strip() if response.css(
                'div[data-id]::text').get() else None,
            'other_info': response.css('div.column-right__inner')[1].css('*::text').get().strip() if len(
                response.css('div.column-right__inner')) > 1 else None,
            'phone_numbers': response.css('div.info-about__phones span::text').getall(),
            'email': response.css('div.info-about__emails span::text').get(),
            'address': response.css('div.info-about__address span::text').get(),
            'languages': response.css('div.languages__list span::text').getall(),
            'education': response.css('div.education span::text').getall(),
            'membership': response.css('div.membership span::text').getall(),
        }
