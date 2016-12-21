# -*- coding: UTF-8 -*-
# -----------------------------------------------------------------------------
#     Contributed by Erik van Blokland and Jonathan Hoefler#     Original from filibuster.#
#     P A G E B O T
#
#     Licensed under MIT conditions
#     Made for usage in DrawBot, www.drawbot.com
# -----------------------------------------------------------------------------
#
# FILIBUSTER.ORG!

"""
        living
--------------------------------------------------------------------
"""

__version__ = '3.0.0'
__author__ = "someone"

content = {
    'books_section': ['Book', 'Book', 'New in print', 'e-Books', 'Magazine', 'Weekly',
        'Opinion', 'New', 'Subscriptions', 'Authors', 'Typography', 'Goodies',
        'Design', 'Interior', 'Education', 'Thriller', 'Sci-Fi', 'Adventure', 'Travel',
        'Parental', 'Kids', 'School', 'Surprise', '<#name#>','<#name#>','<#name#>',
        'Fantasy', 'Detective', 'Horror', 'Classics', 'Children books', 'AAA', 'Elderly',
        'Health and Home', 'Food', 'Healthy cooking', 'Valentine', 'Graduation',
        '<#portal_anyshortname#>',
        '<#portal_anyshortname#>',
        '<#portal_anyshortname#>',
        '<#portal_anyshortname#>',],
    'book_phylosophy_title': [
        '<#book_title_front#> <#book_title_adjective#> <#book_title_end#>',
    ],
    'book_title_adjective': [
        'Metaphysical',
        'Transcendental',
        'Empirical',
        'Axiological',
        'Fundemental',
        'Phenomenologal',
        'Programmatic',
        'Ecological',
    ],
    'book_title_end': [
        'Consciousness and Self-Consciousness:',
        'Thought Rendered Defenseless',
        'Constructing the Relational Mind',
        'Husserlian Phenomenology Meets',
        'Cognitive Science',
        'Phenomenology of Embodiment',
        'Quantum Theory',
        'Realistic Truth Relativism',
        'Non-Human Species',
        'Frameworks of Belief and Conceptual Schemes',
    ],
    'book_title_front': [
        'The science of',
        'The Future of',
        'A reply to',
        'Meditations on',
        'Principles of',
        'The Condition of',
        'Programmatic Arguments of',
        'Defense of the',
        'The Current Relevance of',
        'The Experience of',
        'On the Intrinsic Value of',
        'Universal Law and',
        'The metaphysical Elements of',
        'Introduction to the ',
        'Critique of',
        'Fundemental Principles of',
        'What is',
        'History of',
    ],
    'edition': [
        '(<#language_version#> tr.)',
        '(Original <#language_version#> version of the above)',
        '(Revised)',
        '(partial tr.)',
        '(Commented edition)',
        '(<#language_version#> tr.)',
        '(pirate edition)',
        '(with Postcript)',
        '(The Signed First Edition)',
        '(from the <#year#> ed.)',
        '<#figs_ord#> revised edition',
    ],
    'language_version': [
        'Japanese',
        'English',
        'Hebrew',
        'Arabic',
        'German',
        'Dutch',
        'Italian',
        'Chinese',
        'Spanish',
        'Portugese',
    ],
    'name_arabic': [
        '<#names_first_arabic#> <#names_middle_arabic#> <#names_last_arabic#>',
    ],
    'name_british_science': [
        '<#names_first_British_scientist#> <#names_middle_British_scientist#> <#names_last_British_scientist#>',
    ],
    'names_first_British_scientist': [
        'Kevin',
        'Illtyd',
        'Hubert',
        'Jeremy',
        'Abraham',
        'Otto',
        'Oscar',
        'Henry',
        'Edward',
        'Morris',
        'Thomas',
        'Anthony',
    ],
    'names_first_arabic': [
        'Abu',
        'Abu&amp;#146;l-Hasan',
        'Mohammad',
        'Ahmad',
        'Ahmed',
        'Al-',
    ],
    'names_last_British_scientist': [
        'Balliol',
        'St. James',
        'St. John-Smythe',
        'Warburton',
        'Welby',
        'Northmore',
        'Pugh',
        'Sinclair',
    ],
    'names_last_arabic': [
        'Abd',
        'Allah',
        'Muhammad',
        'Al-Mahani',
        'Yunus',
        'Al-Khujandi',
        'Shuja',
        'Khalaf',
        'al-Jiss',
        'Al-Uqlidisi',
        'Al-Buzjani',
        'al-Sadafi',
        'al-Misri',
        'Abu&amp;#146;l-Wafa',
    ],
    'names_middle_British_scientist': [
        'Ronald',
        'Jeffrey',
        'Herbert',
        'Daniel',
        'Peter',
        'Otto',
        'Ken',
        'Alvin',
        'Neal',
        'Robert',
        'Ismay',
        'Ramon',
    ],
    'names_middle_arabic': [
        'Yunus',
        'ibn',
        'Kamil',
        'Hasan',
        'Abu&amp;#146;l-Wafa',
        'Ali',
        'Jabir',
        'Isa',
        'al-Khidr',
        'Abu l-Wafa',
    ],
    'names_title_British_scientist': [
        'Professor',
        'sir',
        'Dr.',
        'Professor Emeritus',
    ],
    'num_ISDN': [
        'ISDN: <-randint(0, 9)-> <-randint(10000, 99999)-> <-randint(10, 99)-> <-randint(1, 9)->',
    ],
    'page_number': [
        '<-randint(5, 900)->',
        'p.',
    ],
    'publisher_english': [
        'Hutchinson and Cambridge: Harvard University Press',
        'Macmillan: London',
        'Oklahoma University',
        'Bloomington, London',
        'Secker &amp; Warburg, Kent',
        'Cambridge MA: Bradford/MIT Press',
        'Swinburne University of Technology',
        'Unman Hyman: London',
        'Oxford University Press',
        'Thoemmes Press',
        'University of Pennsylvania Press, Philadelphia',
        'Thoemmes Press, Bristol, U.K. and Washington, D.C.',
        'Cornell University Press, Ithaca, New York',
        'Routledge and Kegan Paul',
        'Plenum Publishing, New York',
    ],
    'publisher_int': [
        'Einaudi Milano',
        'F.M. Ricci: Torino',
        'Bompiani: Roma',
        'Livre de Poche, Paris',
        'Izdavatelstvo Pravda, Moskva',
        'Inostrannaja Literatura: Sankt-Peterburg',
        'Ekdotikos Organismos: Thessalonikes',
        'Panstwowy Instytut Wydawniczy, Warszawa',
        'Ylioppilaspaveln: Helsinki',
        'Can Yayinlari: Istanbul',
        'Europa Könyvkiado, In Nagy Vilag, Budapest',
        'Botimet Elena Gjika: Tirana',
        'Ekdoseis Gnose: Athenai',
        'Biblioteca e Centro di Studi a Roma',
        'Izvestiya Akad. Nauk SSSR',
    ],
    'reference_english': [
        '<#name_british_science#>, <#book_phylosophy_title#>, <#publisher_english#>, <#edition#>, <#year#>, <#page_number#>, <#num_ISDN#>',
    ],
    'year': [
        '<-randint(1486, 1999)->',
    ],
    'year_16century': [
        '<-randint(1501, 1599)->',
    ],
    'year_20century': [
        '<-randint(1901, 1999)->',
    ],
    }

