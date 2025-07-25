import xml.etree.ElementTree as ET

def parse_paper_details(xml_data: str):
    root = ET.fromstring(xml_data)
    article = root.find(".//PubmedArticle")

    if article is None:
        return {}

    pmid = article.findtext(".//PMID")
    title = article.findtext(".//ArticleTitle")
    pub_date = article.findtext(".//PubDate/Year")
    if pub_date is None:
        pub_date = article.findtext(".//PubDate/MedlineDate")

    author_list = article.findall(".//Author")
    non_academic_authors = []
    company_affiliations = []
    corresponding_author_email = ""

    for author in author_list:
        affiliation = author.findtext(".//AffiliationInfo/Affiliation")
        email = ""
        if affiliation and "@" in affiliation:
            email = affiliation.split()[-1]
            if email.endswith("@"):
                email = ""
        if email and not corresponding_author_email:
            corresponding_author_email = email
        if affiliation and "pharma" in affiliation.lower():
            company_affiliations.append(affiliation)
        if affiliation and "university" not in affiliation.lower():
            non_academic_authors.append(author.findtext("LastName"))

    return {
        "PubmedID": pmid,
        "Title": title,
        "Publication Date": pub_date,
        "Non-academic Author(s)": ", ".join(filter(None, non_academic_authors)),
        "Company Affiliation(s)": ", ".join(filter(None, company_affiliations)),
        "Corresponding Author Email": corresponding_author_email
    }