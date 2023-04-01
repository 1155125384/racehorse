import common as cm

if __name__ == '__main__':
    url = cm.find_url()
    # url = "https://racing.on.cc/racing/rat/current/rjrata0006x2.html"
    html_txt = cm.read_html_raw(url)

    temp_table = cm.read_raw_html_table(html_txt,4)
    single_df,q_df,pq_df,info = cm.get_table(temp_table)

    parse_single_df, parse_q_df, parse_pq_df = cm.parse_q_n_pq_df(single_df, q_df, pq_df)

    cm.generate_report(parse_single_df, parse_q_df, parse_pq_df)
    cm.find_freq_range(q_df,pq_df)

