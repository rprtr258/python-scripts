// This is an independent project of an individual developer. Dear PVS-Studio, please check it.
// PVS-Studio Static Code Analyzer for C, C++ and C#: http://www.viva64.com
//#include "BigInteger.h"
//
//BigNumber::BigNumber(int n) {
//    while(n > 0) {
//        data_.push_back(n % BASE);
//        n /= BASE;
//    }
//}
//
//BigNumber BigNumber::operator+(const BigNumber &y) const {
//    BigNumber result;
//    long long int carrier = 0;
//    for(auto i = 0u; i < std::max(y.data_.size(), data_.size()); ++i) {
//        long long xx = i >= data_.size() ? 0 : data_[i];
//        long long yy = i >= y.data_.size() ? 0 : y.data_[i];
//        long long r = 0ULL + xx + yy + carrier;
//        result.data_.push_back(r % BASE);
//        carrier = r / BASE;
//    }
//    if(carrier != 0)
//        result.data_.push_back(carrier);
//    return result;
//}
//
//BigNumber BigNumber::operator-(const BigNumber &y) const {
//    BigNumber result;
//    long long carrier = 0;
//    for(auto i = 0u; i < std::max(y.data_.size(), data_.size()); ++i) {
//        long long xx = i >= data_.size() ? 0 : data_[i];
//        long long yy = i >= y.data_.size() ? 0 : y.data_[i];
//        if(0LL + xx >= 0LL + yy + carrier) {
//            result.data_.push_back(xx - yy - carrier);
//            carrier = 0;
//        } else {
//            result.data_.push_back(BASE + xx - yy - carrier);
//            carrier = 1;
//        }
//    }
//    return result;
//}
//
//BigNumber BigNumber::operator*(const BigNumber &y) const {
//    BigNumber result;
//    for(auto i = 0u; i < y.data_.size(); ++i) {
//        long long carrier = 0;
//        BigNumber k;
//        for(auto j = 0u; j < i; ++j)
//            k.data_.push_back(0);
//        for(auto j = 0u; j < data_.size(); ++j) {
//            long long xx = data_[j];
//            long long yy = y.data_[i];
//            long long r = 1ULL * xx * yy + carrier;
//            k.data_.push_back(r % BASE);
//            carrier = r / BASE;
//        }
//        if(carrier != 0)
//            k.data_.push_back(carrier);
//        result = result + k;
//    }
//    return result;
//}
//
//BigNumber BigNumber::operator/(const BigNumber &y) const {
//    BigNumber result;
//    BigNumber l;
//    for(auto i = 0u; i < data_.size(); ++i) {
//        l.data_.push_front(data_[data_.size() - i - 1]);
//        auto div = findDiv(l, y);
//        result.data_.push_front(div);
//        l = l - y * BigNumber(div);
//    }
//    return result;
//}
//
//BigNumber BigNumber::operator%(const BigNumber &y) const {
//    BigNumber l;
//    for(auto i = 0u; i < data_.size(); ++i) {
//        l.data_.push_front(data_[data_.size() - i - 1]);
//        auto div = findDiv(l, y);
//        l = l - y * BigNumber(div);
//    }
//    return l;
//}
//
//bool BigNumber::isZero() const {
//    for(auto i: data_)
//        if(i != 0)
//            return false;
//    return true;
//}
//
//
//bool BigNumber::operator<(const BigNumber &y) const {
//    for(int i = std::max(data_.size(), y.data_.size()) - 1; i >= 0; --i) {
//
//        auto xx = i >= static_cast<int>(data_.size()) ? 0 : data_[i];
//        auto yy = i >= static_cast<int>(y.data_.size()) ? 0 : y.data_[i];
//        if(xx != yy)
//            return xx < yy;
//    }
//    return false;
//}
//
//
//unsigned BigNumber::findDiv(const BigNumber &dividend, const BigNumber &divisor) const {
//    unsigned first = 0;
//    unsigned last = BASE;
//
//    unsigned it;
//    int64_t count, step;
//    count = last - first;
//    while(count > 0) {
//        it = first;
//        step = count / 2;
//        it += step;
//        if(!(dividend < BigNumber(it) * divisor)) {
//            first = ++it;
//            count -= step + 1;
//        } else
//            count = step;
//    }
//    return first - 1;
//}
//
//void BigNumber::print(std::ostream &s) const {
//    std::string result;
//    auto x(*this);
//    while(!x.isZero()) {
//        auto n = (x % 10).data_[0];
//        result = (char)(n + '0') + result;
//        x = x / 10;
//    }
//    if(result.empty())
//        s << "0";
//    else
//        s << result;
//}
//
//std::ostream &operator<<(std::ostream &s, const BigNumber &n) {
//    n.print(s);
//    return s;
//}
