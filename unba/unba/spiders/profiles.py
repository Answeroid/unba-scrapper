import scrapy
import requests


class ProfilesSpider(scrapy.Spider):
    name = "profiles"
    allowed_domains = ["erau.unba.org.ua"]
    base_url = "https://erau.unba.org.ua/profile"

    def start_requests(self):
        existing_profiles = []

        for profile_number in range(1, 100001):
            url = f"{self.base_url}/{profile_number}"
            response = requests.get(url)

            if response.status_code != 200 and "На жаль, такої сторінки не існує" not in response.text:
                self.log(f"Profile {profile_number} exists!")
                existing_profiles.append(profile_number)
                yield scrapy.Request(url=url, callback=self.parse_profile)

        if existing_profiles:
            self.log("Existing Profiles: " + ', '.join(map(str, existing_profiles)))
        else:
            self.log("No existing profiles found.")

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
            'term_right_info': response.css('div[data-id]::text').get().strip(),
            'other_info': response.css('div.column-right__inner')[1].css('*::text').get().strip() if len(
                response.css('div.column-right__inner')) > 1 else None,
            'phone_numbers': response.css('div.info-about__phones span::text').getall(),
            'email': response.css('div.info-about__emails span::text').get(),
            'address': response.css('div.info-about__address span::text').get(),
            'languages': response.css('div.languages__list span::text').getall(),
            'education': response.css('div.education span::text').getall(),
            'membership': response.css('div.membership span::text').getall(),
        }
