export default {
    preset: 'ts-jest',
    testEnvironment: 'node',
    moduleFileExtensions: ['js', 'ts', 'vue'],
    transform: {
        '^.+\\.ts$': 'ts-jest',
        '^.+\\.vue$': 'vue-jest',
        '^.+\\.js$': 'babel-jest',
    },
    transformIgnorePatterns: ['<rootDir>/node_modules/'],
    moduleNameMapper: {
        '^@/(.*)$': '<rootDir>/$1',
    },
};