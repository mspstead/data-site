import word_cloud_generator as wcg
trump_urls = ["https://www.reddit.com/r/The_Donald/comments/4uxdbn/im_donald_j_trump_and_im_your_next_president_of/",
            "https://www.reddit.com/r/The_Donald/comments/5bzjv5/donald_j_trump_declared_the_winner/",
            "https://www.reddit.com/r/The_Donald/comments/5jt9xs/cnn_will_soon_be_1when_searching_for_the_term/",
            "https://www.reddit.com/r/The_Donald/comments/5bz5ds/all_celebrities_that_vowed_to_leave_the_usa_if/",
            "https://www.reddit.com/r/The_Donald/comments/5byneu/imminent_victory_thread/",
            "https://www.reddit.com/r/The_Donald/comments/5cxunu/its_official_trump_will_become_the_first_us/",
            "https://www.reddit.com/r/The_Donald/comments/5c2t5d/press_f_to_pay_respect/",
            "https://www.reddit.com/r/The_Donald/comments/5cax76/youtube_removed_countless_copies_of_this_video_of/",
            "https://www.reddit.com/r/The_Donald/comments/5tqp0b/her_name_is_nazi_paikidze_and_shes_the_united/",
            "https://www.reddit.com/r/The_Donald/comments/5fsgz9/when_you_tear_out_a_mans_tongue_you_havent_proved/",
            "https://www.reddit.com/r/The_Donald/comments/59vld8/this_just_in_from_chaffetz_fbi_dir_just_informed/",
            "https://www.reddit.com/r/The_Donald/comments/5oy456/reddit_admins_are_you_salty_%E0%B2%A5%E0%B2%A5/",
            "https://www.reddit.com/r/The_Donald/comments/5pqd6o/bernie_sanders_praises_trump_for_tpp_withdrawal/",
            "https://www.reddit.com/r/The_Donald/comments/5frrsz/ceo_of_reddit_just_called_us_toxic_users_and_a/",
            "https://www.reddit.com/r/The_Donald/comments/5byi69/victory_for_president_trump/"]

bernie_urls = ["https://www.reddit.com/r/SandersForPresident/comments/fdih22/bernie_sanders_calls_on_joe_biden_to_agree_to_a/",
               "https://www.reddit.com/r/SandersForPresident/comments/5p1syn/shouldve_been_bernie/",
               "https://www.reddit.com/r/SandersForPresident/comments/fuagnl/we_need_a_revolution/",
               "https://www.reddit.com/r/SandersForPresident/comments/ftn6az/prophecy/",
               "https://www.reddit.com/r/SandersForPresident/comments/c26oqw/i_am_senator_bernie_sanders_ask_me_anything/",
               "https://www.reddit.com/r/SandersForPresident/comments/f2konn/bernie_sanders_wins_new_hampshire_primary/",
               "https://www.reddit.com/r/SandersForPresident/comments/fj0n0j/hours_before_bernies_most_important_career_debate/",
               "https://www.reddit.com/r/SandersForPresident/comments/fx8j4w/its_over_sadly_heartbroken_we_needed_him_more/",
               "https://www.reddit.com/r/SandersForPresident/comments/fdcdlc/if_we_want_bernie_to_win_young_voters_have_to/",
               "https://www.reddit.com/r/SandersForPresident/comments/f9btod/basketball_and_baseball_for_the_win/",
               "https://www.reddit.com/r/SandersForPresident/comments/ffii33/radical_idea_alert/",
               "https://www.reddit.com/r/SandersForPresident/comments/fle3vc/well_said/",
               "https://www.reddit.com/r/SandersForPresident/comments/cn6y2v/you_pay_more_tax_than_amazon/",
               "https://www.reddit.com/r/SandersForPresident/comments/focs3h/bernie_sanders_wins_utah_presidential_primary/",
               "https://www.reddit.com/r/SandersForPresident/comments/enrtf2/were_gonna_win/"]

trump_mask_file = 'word_mask_silhouettes/trump.jpg'
bernie_mask_file = 'word_mask_silhouettes/bernie_sil.jpg'

wcg.create_word_cloud(bernie_urls,bernie_mask_file)
wcg.create_word_cloud(trump_urls,trump_mask_file)

