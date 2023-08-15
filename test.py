import requests
import openai

# OpenAI API Configuration
openai.api_key = 'YOUR_OPENAI_API_KEY'

# 1. Technology Detection
def detect_technology(domain):
    technologies = []
    
    # WordPress Detection
    try:
        response = requests.get(f"{domain}/wp-login.php")
        if 'WordPress' in response.text:
            technologies.append('WordPress')
    except:
        pass

    # Joomla Detection
    try:
        response = requests.get(f"{domain}/administrator/manifests/files/joomla.xml")
        if 'joomla' in response.text.lower():
            technologies.append('Joomla')
    except:
        pass

    # Drupal Detection
    try:
        response = requests.get(f"{domain}/CHANGELOG.txt")
        if 'drupal' in response.text.lower():
            technologies.append('Drupal')
    except:
        pass
    
    # Magento Detection
    try:
        response = requests.get(f"{domain}/app/Mage.php")
        if 'Magento' in response.text:
            technologies.append('Magento')
    except:
        pass

    return technologies

# 2. Leverage Existing Wordlists (SecLists)
def get_wordlist_from_seclists(technologies):
    wordlist = set()

    # WordPress
    if 'WordPress' in technologies:
        with open('path_to_SecLists/Discovery/Web-Content/wordpress.txt', 'r') as f:
            wordlist.update(f.readlines())

    # Joomla
    if 'Joomla' in technologies:
        with open('path_to_SecLists/Discovery/Web-Content/joomla.txt', 'r') as f:
            wordlist.update(f.readlines())

    # Drupal
    if 'Drupal' in technologies:
        with open('path_to_SecLists/Discovery/Web-Content/drupal.txt', 'r') as f:
            wordlist.update(f.readlines())
            
    # Magento
    if 'Magento' in technologies:
        with open('path_to_SecLists/Discovery/Web-Content/magento.txt', 'r') as f:
            wordlist.update(f.readlines())

    return wordlist




# 2. Leverage Existing Wordlists (SecLists)
def get_wordlist_from_seclists(technologies):
    wordlist = set()

    # WordPress
    if 'WordPress' in technologies:
        with open('path_to_SecLists/Discovery/Web-Content/wordpress.txt', 'r') as f:
            wordlist.update(f.readlines())

    # TODO: Add other technology-specific lists as needed

    return wordlist


# 3. Passive Data Collection
def fetch_from_robots_txt(domain):
    paths = set()
    try:
        response = requests.get(f"{domain}/robots.txt")
        for line in response.text.split("\n"):
            if "Disallow" in line or "Allow" in line:
                paths.add(line.split(": ")[1].strip())
    except:
        pass
    return paths


# 4. AI-enhanced Predictions
def generate_wordlist_with_llm(data_points):
    prompt = f"Based on the following paths from a website: {', '.join(list(data_points)[:5])}... predict other potential paths."
    response = openai.Completion.create(engine="davinci", prompt=prompt, max_tokens=200)
    return set(response.choices[0].text.strip().split('\n'))


# 5. Dynamic Generation
def user_input_keywords():
    keywords = input("Enter any specific keywords or themes (comma-separated): ")
    return set(keywords.split(","))


# 6. Filter and Deduplicate
def compile_wordlist(*args):
    combined = set().union(*args)
    return combined


def main(domain):
    techs = detect_technology(domain)
    seclists_words = get_wordlist_from_seclists(techs)
    robots_txt_paths = fetch_from_robots_txt(domain)
    llm_words = generate_wordlist_with_llm(robots_txt_paths)
    user_words = user_input_keywords()
    
    final_wordlist = compile_wordlist(seclists_words, robots_txt_paths, llm_words, user_words)
    
    # Save to a file or return
    with open("final_wordlist.txt", "w") as f:
        for entry in final_wordlist:
            f.write(entry + "\n")

    print(f"Wordlist saved as final_wordlist.txt with {len(final_wordlist)} entries.")


if __name__ == "__main__":
    target_domain = input("Enter the target domain (e.g., https://example.com): ")
    main(target_domain)



# ... (rest of the functions and main script)
