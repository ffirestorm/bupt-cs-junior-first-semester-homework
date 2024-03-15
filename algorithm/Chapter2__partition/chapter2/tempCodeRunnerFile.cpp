    for (int i = 0 ; i < datas.size() ; i++){
        result = select(datas, 0, datas.size()-1, i+1);
        cout << i+1 <<"." <<result.ENODEBID << ": " << result.K_DIST<<endl;
    }